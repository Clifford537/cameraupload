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
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE , default=1)  # Link to user
    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('file',)

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.course}"

class UploadedImage(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE)  # Link to user, allow null
    image = models.ImageField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"
