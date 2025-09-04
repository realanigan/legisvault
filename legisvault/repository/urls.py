from django.urls import path
from . import views



urlpatterns = [
    path("", views.indexview, name="index"),
    path("aboutus", views.aboutUsView, name="aboutus"),
    path("publications", views.publicationView, name="publications"),
    path("publications/<str:publication>", views.publicationListing, name="publication-listing"),
    path("publications/<str:publication>/<str:id>/<slug:slug>", views.publicationDetails, name="publication-details"),
    path("legislator/<int:id>", views.getCouncellor, name="councellor"),
]
