from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Document
from .forms import DocumentForm
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from PIL import Image
import os
from io import BytesIO
from django.views import View


def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if a file with the same content already exists
            uploaded_file = form.cleaned_data.get("file")
            if Document.objects.filter(file=uploaded_file.name).exists():
                messages.error(request, "This document has already been uploaded.")
            else:
                form.save()
                messages.success(request, "File uploaded successfully!")
                return redirect("upload_document")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = DocumentForm()
    
    return render(request, "upload/upload.html", {"form": form})


from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.base import ContentFile
from PIL import Image
import os
from io import BytesIO
from django.views import View
from .models import UploadedImage, ConvertedPDF

class ImageToPDFView(View):
    def get(self, request):
        return render(request, "upload/image_upload.html")  # Simple upload page

    def post(self, request):
        images = request.FILES.getlist("images")  # Get multiple uploaded images
        if not images:
            return HttpResponse("No images uploaded", status=400)

        image_list = []
        for image in images:
            uploaded_image = UploadedImage.objects.create(image=image)  # Save image to DB
            img = Image.open(uploaded_image.image)
            img = img.convert("RGB")  # Ensure compatibility with PDF
            image_list.append(img)

        if image_list:
            pdf_filename = "converted.pdf"
            pdf_bytes = BytesIO()
            image_list[0].save(pdf_bytes, format="PDF", save_all=True, append_images=image_list[1:])
            pdf_bytes.seek(0)

            pdf_model = ConvertedPDF.objects.create()  # Save PDF model instance
            pdf_model.pdf_file.save(pdf_filename, ContentFile(pdf_bytes.read()))
            pdf_model.save()

            response = HttpResponse(pdf_model.pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'
            return response

        return HttpResponse("Error processing images", status=500)
