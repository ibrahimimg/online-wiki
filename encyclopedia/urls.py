from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.random_page, name="wiki"),
    path("wiki/<str:entry>", views.wiki, name="wiki_entry"),
    path("error", views.error, name="error"),
    path("search", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("edit/<str:entry>", views.edit, name="edit")
]
