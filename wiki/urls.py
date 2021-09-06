from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add_page", views.add_page, name="add_page"),
    path("random", views.random, name="random"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
]
