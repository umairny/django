from django.db.models import fields
from django.db.models.fields import CharField
from django.forms import ModelForm, Textarea, FileInput, DateField, TextInput, widgets
from .models import *
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location','birth_date', 'picture']
        widgets = {
            'location' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'your location', 'type':'text'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date', 
                                            'placeholder':'Select a date'}),
            'picture': FileInput(attrs={'class': 'form-control-file'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post',)
        widgets = {
            'post': Textarea(attrs={'class': 'form-control ', 'rows' :'2',
            'placeholder': 'your text goes here'})
        }
