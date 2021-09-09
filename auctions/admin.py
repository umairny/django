from django.contrib import admin
from django.contrib.admin.options import HORIZONTAL
from .models import *

# Register your models here.
class BidAdmin(admin.ModelAdmin):
    list_display = ('user', 'bid', 'list', 'updated')

    
admin.site.register(Listing)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Category)