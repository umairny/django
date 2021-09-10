from django.core.exceptions import ValidationError
from django.db import models
from django.urls.base import reverse
from django.contrib.auth.models import User
from django.conf import settings


#Listing Database
class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=64)
    details = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created = models.DateTimeField(blank=True, auto_now_add=True)

    # Picture
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    #new_Img = models.ImageField(upload_to='images/', null=True, verbose_name="")

    CATEGORY_CHOICES = [
        ('Cloth', 'Cloths'),
        ('Watch', 'Watches'),
        ('Decor', 'Decors'),
        ('Phone', 'Cell Phone'),
        ('Computer', 'Computer'),
        ('Glasses', 'Glasses'),
    ]
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='Cloth',
    )


    closed = models.BooleanField(default=False)

    watchlistuser = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def no_of_bids(self):
        return len(self.bid_list.all())

    def current_winning_bidder(self):
        return self.bid_list.get(bid=self.cur_price()).user if self.no_of_bids() > 0 else None
 
    def cur_price(self):
        return max([bid.bid for bid in self.bid_list.all()]+[self.price])

    def __str__(self):
        return f"{self.id} {self.user} {self.title} {self.details} {self.category} {self.price} {self.picture} {self.closed} {self.watchlistuser}"


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="", related_name="bid_user")
    bid = models.DecimalField(max_digits=5, decimal_places=2, blank=False)
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, default="", related_name="bid_list")
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    def clean(self):
        if self.bid and self.list.cur_price():
            if self.bid <= self.list.cur_price():
                raise ValidationError({'bid': ('Warning!! Your bidding value should be higher than the current price or bid of the item!')})

    def __str__(self):
        return f"{self.id} {self.bid} {self.list} {self.user} {self.updated}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name= "comments", null= True)
    comment = models.TextField()
    com_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.id} {self.comment} {self.com_time} {self.user}"
    
class Category(models.Model):
    field = models.CharField(max_length= 64, default="")

    def __str__(self):
        return self.field
