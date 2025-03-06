from django.db import models

COURSE_CHOICES = [
    ('BSc IT', 'BSc IT'),
    ('BSc IS', 'BSc IS'),
    ('BSc ICTM', 'BSc ICTM'),
    ('BSc CS', 'BSc CS'),
    ('BSc CT', 'BSc CT'),
    ('Diploma in IT', 'Diploma in IT'),
]

class Document(models.Model):
    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('file',)  # Ensures no duplicate files are uploaded

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.course}"

class UploadedImage(models.Model):
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ConvertedPDF(models.Model):
    pdf_file = models.FileField(upload_to="pdfs/")
    created_at = models.DateTimeField(auto_now_add=True)
