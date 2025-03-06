from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['course', 'year', 'title', 'file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            
        # Check if a file with the same name already exists
            if Document.objects.filter(file=file.name).exists():
                raise forms.ValidationError("This file has already been uploaded.")

        return file


