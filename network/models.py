from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings

class Posts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_user")
    post = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(blank=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, default='')

    @property
    def total_likes(self):
        return self.like.count()

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.id,
            "post" : self.post,
            "pub_date": self.pub_date.strftime("%b %d %Y, %I:%M %p"),
            "total_likes": self.total_likes,
            "reply": self.reply,
        }
        
    def __str__(self):
        return f"{self.post} {self.user} {self.pub_date} {self.like} {self.reply}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name="profile_user")
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    picture = models.ImageField(upload_to="site/images/", null=True, blank=True)

    follow = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
        
    def serialize(self):
        return {
            "user": self.user.username,
            "followers": self.follow,   
        }

    def __str__(self):
        return f"{self.id} {self.user} {self.follow} {self.location} {self.birth_date} {self.picture} profile"
