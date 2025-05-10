from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Document, UploadedImage
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def home(request):
    return render(request, 'upload/home.html')
# Handle PDF and other files upload
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # Validate file type
            if uploaded_file.content_type not in ['application/pdf']:
                messages.error(request, "Only PDF files are allowed.")
            else:
                try:
                    form.save()
                    messages.success(request, "PDF uploaded successfully.")
                    return redirect('upload_file')
                except ValidationError as e:
                    messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = DocumentForm()

    # Show uploaded files (including PDFs)
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'upload/upload_file.html', {'form': form, 'documents': documents})

# Handle image upload (JPEG/PNG)
def upload_image(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # Validate file type
            if uploaded_file.content_type not in ['image/jpeg', 'image/png']:
                messages.error(request, "Only JPEG and PNG image files are allowed.")
            else:
                try:
                    form.save()
                    messages.success(request, "Image uploaded successfully.")
                    return redirect('upload_image')
                except ValidationError as e:
                    messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = DocumentForm()

    # Load unique titles from CSV
    data = load_csv_data()
    unique_titles = sorted(set(item['title'] for item in data))

    # Show uploaded images (JPEG/PNG)
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'upload/upload_image.html', {'form': form, 'documents': documents, 'unique_titles': unique_titles})
   
def my_uploads(request):
    # Fetch all documents and images uploaded by the logged-in user
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    images = UploadedImage.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, 'upload/my_uploads.html', {
        'documents': documents,
        'images': images
    })

import csv
import os
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings

# Cache CSV data in memory
CSV_DATA = None

def load_csv_data():
    global CSV_DATA
    if CSV_DATA is None:
        csv_path = os.path.join(settings.BASE_DIR, 'media', 'file1.csv')
        data = []
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Normalize keys and strip whitespace
                data.append({
                    'year': row['year'].strip().lower(),
                    'course': row['course'].strip().lower(),
                    'title': row['title'].strip()
                })
        CSV_DATA = data
    return CSV_DATA



@require_GET
def autocomplete_titles(request):
    query = request.GET.get("query", "").strip().lower()
    course = request.GET.get("course", "").strip().lower()
    year = request.GET.get("year", "").strip().lower()

    filtered_titles = set()
    for item in load_csv_data():
        if item['course'] == course and item['year'] == year and query in item['title'].lower():
            filtered_titles.add(item['title'])

    return JsonResponse({"titles": sorted(filtered_titles)})

