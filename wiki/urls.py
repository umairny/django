from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("sing_search/<str:title>", views.sing_search, name="sing_search"),
    path("sing_search/wiki/edit/<str:title>", views.edit, name="edit"),

    path("add_page", views.add_page, name="add_page"),
    path("random", views.random, name="random"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
]
