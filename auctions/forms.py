from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, FileInput
from .models import Listing, Bid, Comment
from django import forms
import re
from django.core.files.uploadedfile import InMemoryUploadedFile
from .humanize import naturalsize


class MainForm(ModelForm):
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Listing
        fields = ('title', 'details', 'price', 'category', 'picture')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'details': Textarea(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
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
        instance = super(MainForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': Textarea(attrs={'class': 'form-control', 'rows':'2',
            'placeholder': 'comment here'})
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']


