from django.urls import path
from . import views
from .views import ImageToPDFView

urlpatterns = [
    path("document/", views.upload_document, name="upload_document"),
    path("", ImageToPDFView.as_view(), name="image_to_pdf"),

]
