from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from . import views

app_name='network'
urlpatterns = [
    path("", views.index, name="index"),
    #path("login", views.login_view, name="login"),
    #path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

   # API Routes
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("like/<int:post_id>", views.like, name="like"),

    # extra routes
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),
    path("profile/edit/<int:post_id>", views.edit, name="edit"),
    path("profile/comment/<int:post_id>", views.comment, name="comment"),
    path("profile/like/<int:post_id>", views.like, name="like"),


    #Picture urls
    path('prof_picture/<int:pk>', views.stream_file, name='prof_picture'),
    
    #follow
    path("<int:user_id>/follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
]

