from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.entry, name="entry"),
    path("edit/<title>", views.edit, name="edit"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add"),
    path("random/", views.random, name="random"),
]
