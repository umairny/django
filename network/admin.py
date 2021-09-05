from django.forms.models import modelform_factory
from .views import register
from django.contrib import admin
from .models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('follow',)

admin.site.register(Posts)
admin.site.register(Profile, ProfileAdmin)

