from heapq import merge

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from pathlib import Path
import os
from django.template import loader
from .forms import PhotoForm
from django.shortcuts import redirect
from .models import Photo

import cv2
from fontTools.misc.classifyTools import classify
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
from isbnlib import *

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def home(request):
    if request.method == 'POST':
        os.system('rm -rf media/uploads/*')
        Photo.objects.filter(image='uploads/code.jpg').delete()
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/home/bookDetails')
    else:
        form = PhotoForm()
    return render(request, 'home.html', {'form': form})

def scan(request):
    return render(request, 'scan.html')

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

def bookDetails(request):


    photo = Photo.objects.get(image='uploads/code.jpg')  # or .latest('uploaded_at')
    full_path = photo.image.path  # THIS is the full path that cv2 needs

    image = cv2.imread(full_path)
    barcode = detect_and_decode_barcode(image)
    service = 'openl'



    if barcode == -1:
        print("No barcode found")
    else:
        print(meta(barcode, service), "\n")
        bookData = meta(barcode, service)
        try:
            coverTh = cover(barcode)['thumbnail']
        except:
            coverTh = '/static/missingCover.png'

    template = loader.get_template('book.html')
    context = {
        'title': bookData['Title'],
        'bookData': bookData,
        'cover': coverTh,
    }

    return HttpResponse(template.render(context, request))