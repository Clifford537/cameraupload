from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Document
from .forms import DocumentForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Document, UploadedImage


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

    # Show uploaded images (JPEG/PNG)
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'upload/upload_image.html', {'form': form, 'documents': documents})
def my_uploads(request):
    # Fetch all documents and images uploaded by the logged-in user
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    images = UploadedImage.objects.filter(user=request.user).order_by('-uploaded_at')

    return render(request, 'upload/my_uploads.html', {
        'documents': documents,
        'images': images
    })