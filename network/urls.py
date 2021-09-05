from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("  network/login", views.login_view, name="login"),
    path("network/logout", views.logout_view, name="logout"),
    path("network/register", views.register, name="register"),

   # API Routes
    path("network/edit/<int:post_id>", views.edit, name="edit"),
    path("network/comment/<int:post_id>", views.comment, name="comment"),
    path("network/like/<int:post_id>", views.like, name="like"),

    # extra routes
    path("network/profile/<int:user_id>", views.profile, name="profile"),
    path("network/edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),

    #Picture urls
    #path('net_picture/<int:pk>', views.stream_file, name='net_picture'),
    
    #follow
    path("network/<int:user_id>/follow", views.follow, name="follow"),
    path("network/following", views.following, name="following"),
]

