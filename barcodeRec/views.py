from heapq import merge

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from pathlib import Path
import os
from django.template import loader
from .forms import PhotoForm
from django.shortcuts import redirect
from .models import Photo, Book, Rating

import cv2
from fontTools.misc.classifyTools import classify
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
from isbnlib import *

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login')
    if request.method == 'POST':
        os.system('rm -rf media/uploads/*')
        Photo.objects.filter(image='uploads/code.jpg').delete()
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/home/scanBook')
    else:
        form = PhotoForm()
    return render(request, 'home.html', {'form': form})


def detect_and_decode_barcode(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect barcodes in the grayscale image
    barcodes = decode(gray)


    if len(barcodes) == 0:
        return -1
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data and type
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # Print barcode data and type
        print("Barcode Data:", barcode_data)
        print("Barcode Type:", barcode_type)

        # Draw a rectangle around the barcode
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Put barcode data and type on the image
        cv2.putText(image, f"{barcode_data} ({barcode_type})",
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Convert image from BGR to RGB (Matplotlib uses RGB)
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # plt.imshow(image_rgb)
    # plt.axis('off')
    # plt.show()

    return barcode_data


def scanCode(request):
    try:
        photo = Photo.objects.latest('uploaded_at')
    except Photo.DoesNotExist:
        return HttpResponse("No uploaded photo found. Please scan a book first.")
    full_path = photo.image.path
    image = cv2.imread(full_path)
    barcode = detect_and_decode_barcode(image)

    return redirect('/home/bookDetails/?isbn=' + barcode)

def bookDetails(request):
    barcode = -1

    barcode = request.GET.get('isbn')
    print("Method get")
    service = 'openl'

    bookData = {}
    coverTh = '/static/missingCover.png'

    if barcode != -1:
        try:
            bookData = meta(barcode, service)
            title = bookData.get('Title', 'Unknown Title')
            author = ', '.join(bookData.get('Authors', []))
            # isbn = bookData.get('ISBN-13', barcode)
            isbn = barcode
            try:
                coverTh = cover(barcode)['thumbnail']
            except:
                pass

            # Book.objects.get_or_create(
            #     isbn=barcode,
            #     defaults={'title': title, 'author': author}
            # )

        except Exception as e:
            print("Error retrieving book data:", e)

    if request.method == "POST":
        isbn = request.POST['code']
        action = request.POST['action']

        if action == 'reviewBook':
            rating_value = int(request.POST['rating'])
            Rating.objects.update_or_create(
                user=request.user,
                isbn=barcode,
                defaults={'rating': rating_value}
            )

        if action == 'addToLibrary':
            Book.objects.update_or_create(
                user = request.user,
                title = title,
                author = author,
                isbn = barcode
            )
        elif action == 'returnBook':
            returnBook(isbn, request.user)
        elif action == 'addToWishlist':
            addToWishlist(isbn, request.user)

        return redirect(request.path)
    
    existing_rating = Rating.objects.filter(user=request.user, isbn=barcode).first()
    context = {
        'title': bookData.get('Title', 'Unknown'),
        'code': bookData.get('ISBN-13', barcode),
        'bookData': bookData,
        'cover': coverTh,
        'existing_rating': existing_rating.rating if existing_rating else 0,
    }

    return render(request, 'book.html', context)


def addToLibrary(isbn, user):
    pass

def returnBook(isbn, user):
    pass

def addToWishlist(isbn, user):
    pass
