from django.db.models import fields
from django.db.models.fields import CharField
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import ModelForm, Textarea, FileInput, DateField, TextInput, widgets
from .models import *
from django import forms
from .humanize import naturalsize

class ProfileForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Profile
        fields = ['full_name', 'location','birth_date', 'picture']
        widgets = {
            'full_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Full Name', 'type':'text'}),
            'location' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'your location', 'type':'text'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date', 
                                            'placeholder':'Select a date'}),
        }

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
        if pic is None:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(ProfileForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post',)
        widgets = {
            'post': Textarea(attrs={'class': 'form-control ', 'rows' :'2',
            'placeholder': 'your text goes here'})
        }
