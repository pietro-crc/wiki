
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("wiki/<str:title>", views.util.get_entry, name="get_entry"),
]
