from django import forms
from .models import Document

YEAR_CHOICES = [
    ('year 1', 'year 1'),
    ('year 2', 'year 2'),
    ('year 3', 'year 3'),
    ('year 4', 'year 4'),
]

COURSE_CHOICES = [
    ('information technology', 'information technology'),
    ('information systems', 'information systems'),
    ('ictm', 'ictm'),
    ('computer science', 'computer science'),
    ('computer technology', 'computer technology'),
    ('diploma in it', 'diploma in it'),
]

class DocumentForm(forms.ModelForm):
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    course = forms.ChoiceField(choices=COURSE_CHOICES)

    class Meta:
        model = Document
        fields = ['course', 'year', 'title', 'file']
