from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("listing/<int:list_id>", views.listing, name= "listing"),
    path("comment/<int:list_id>", views.comment, name="comment"),
    path("watchlist/<int:list_id>", views.watchlist, name="watchlist"),
    path("watchlistitems", views.watchlistitems, name="watchlistitems"),
    path("closed/<int:list_id>", views.closed, name="closed"),
    path("categories/<str:category>", views.category, name='category'),
    path("categories", views.categories, name="categories"),

    #Picture urls
    path('list_picture/<int:pk>', views.stream_file, name='list_picture'),

]
