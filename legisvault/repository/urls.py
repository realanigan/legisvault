from django.urls import path
from . import views



urlpatterns = [
    path("", views.indexview, name="index"),
    path("aboutus", views.aboutUsView, name="aboutus"),
    path("publications", views.publicationView, name="publications"),
    path("publications-section", views.publicationSectionView, name="publications-section"),
]
