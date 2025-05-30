import csv
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from pathlib import Path
import os
from django.template import loader
from userProfile.decorators import user_type_required
from .forms import PhotoForm
from .models import Photo, Book, Rating
import cv2
from pyzbar.pyzbar import decode
from isbnlib import *
import random
from .map_headers import map_headers, EXPECTED_FIELDS

BASE_DIR = Path(__file__).resolve().parent.parent

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
    return render(request, 'home.html', {'form': form, 'random_number': random.randint(0, 7)})


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
            description = desc(barcode)
            print(description)
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
            # Rating.objects.update_or_create(
            #     user=request.user,
            #     title=title,
            #     isbn=barcode,
            #     defaults={'rating': rating_value}
            # )

            if Rating.objects.filter(isbn=barcode, user=request.user):
                oldRating = Rating.objects.filter(isbn=barcode, user=request.user).values('rating')[0]['rating']  #save old user rating
                Rating.objects.filter(isbn=barcode, user=request.user).update(rating=rating_value)  #update to new user rating
                numberOfRatings = Rating.objects.filter(isbn=barcode, user=request.user).values('number_of_ratings')[0]['number_of_ratings']  #save number of ratings
                oldTotalRating = Rating.objects.filter(isbn=barcode, user=request.user).values('total_rating')[0]['total_rating']      #save old total rating

                updatedTotalRating = "{:.2f}".format((oldTotalRating * numberOfRatings - oldRating + rating_value)/numberOfRatings)

                Rating.objects.filter(isbn=barcode).update(total_rating=updatedTotalRating)  #update new total rating
                print("Rating updated")
            else:
                if Rating.objects.filter(isbn=barcode):

                    currentTotalRating = Rating.objects.filter(isbn=barcode).values('total_rating')[0]['total_rating']
                    currentNoOfRatings = Rating.objects.filter(isbn=barcode).values('number_of_ratings')[0]['number_of_ratings']

                    Rating.objects.filter(isbn=barcode).update(number_of_ratings=currentNoOfRatings+1)

                    updatedTotalRating = "{:.2f}".format((currentTotalRating*currentNoOfRatings+rating_value)/(currentNoOfRatings+1))
                    Rating.objects.filter(isbn=barcode).update(total_rating=updatedTotalRating)

                    Rating.objects.update_or_create(
                        user=request.user,
                        title=title,
                        isbn=barcode,
                        total_rating=updatedTotalRating,
                        number_of_ratings=currentNoOfRatings+1,
                        defaults={'rating': rating_value}
                    )
                else:
                    Rating.objects.update_or_create(
                        user=request.user,
                        title=title,
                        isbn=barcode,
                        total_rating=rating_value,
                        number_of_ratings=1,
                        defaults={'rating': rating_value}
                    )
                    print("Rating created")
            return redirect('/profile/my-ratings/')

        if action == 'addToLibrary':
            Book.objects.update_or_create(
                user = request.user,
                title = title,
                author = author,
                isbn = barcode,
                cover = coverTh,
            )
            return redirect('/profile/saved-books/')

        if action == 'returnBook':
            Book.objects.filter(user=request.user, isbn=barcode).delete()
            return redirect('/profile/saved-books/')
    
    existing_rating = Rating.objects.filter(user=request.user, isbn=barcode).first()
    if Rating.objects.filter(isbn=barcode).values('total_rating'):
        total_rating_for_book = Rating.objects.filter(isbn=barcode).values('total_rating')[0]['total_rating']
    else:
        total_rating_for_book = 0

    if Rating.objects.filter(isbn=barcode):
        number_of_ratings_for_book = Rating.objects.filter(isbn=barcode).values('number_of_ratings')[0]['number_of_ratings']
    else:
        number_of_ratings_for_book = 0


    print(total_rating_for_book)
    context = {
        'title': bookData.get('Title', 'Unknown'),
        'code': bookData.get('ISBN-13', barcode),
        'bookData': bookData,
        'description': description,
        'cover': coverTh,
        'existing_rating': existing_rating.rating if existing_rating else 0,
        'in_library': 1 if Book.objects.filter(user=request.user, isbn=barcode) else 0,
        'total_rating': total_rating_for_book,
        'number_of_ratings': number_of_ratings_for_book,
        'random_number': random.randint(0, 7)
    }

    return render(request, 'book.html', context)


@user_type_required("Librarie")
def manage_books(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            messages.error(request, "No file uploaded.")
            return redirect("manage_books")

        if not csv_file.name.endswith(".csv"):
            messages.error(request, "Invalid file format.")
            return redirect("manage_books")

        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        field_map = map_headers(reader.fieldnames)

        if len(field_map) < len(EXPECTED_FIELDS):
            missing = [k for k in EXPECTED_FIELDS if k not in field_map]
            messages.error(request, f"Missing required column(s): {', '.join(missing)}")
            books = Book.objects.filter(user=request.user)

        imported_count = 0
        skipped_count = 0

        for row in reader:
            try:
                title = row.get(field_map.get("title", ""), "").strip()
                author = row.get(field_map.get("author", ""), "").strip()
                isbn = row.get(field_map.get("isbn", ""), "").strip()

                if Book.objects.filter(title=title, author=author, user=request.user).exists():
                    skipped_count += 1
                    continue

                Book.objects.create(title=title, author=author, isbn=isbn, user=request.user)
                imported_count += 1

            except:
                continue

        messages.success(request, f"CSV processed: {imported_count} imported, {skipped_count} skipped (reason: duplicates). ")


    books = Book.objects.filter(user=request.user)

    return render(request, "manageBooks.html", {"books": books})



