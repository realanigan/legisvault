from django.shortcuts import render, get_object_or_404, redirect
from .models import LegislatorTerm, LegalMeasure
from django.http import Http404
from datetime import date

from django.db.models import Case, When, IntegerField

## Custom sort (VM, councilor, etc) for database query result
order = Case(
    When(position='Municipal Vice Mayor', then=1),
    When(position='Councilor', then=2),
    When(position='ABC President', then=3),
    When(position='IP Representative', then=4),
    When(position='SK Municipal Federation President', then=5),
    default=99,  # everything else goes last
    output_field=IntegerField(),
)




def indexview(request):
  return render(request,"home.html",{"request":request})


def aboutUsView(request):
  current_year = date.today().year
  current_legislators = LegislatorTerm.objects.filter(start_of_term__year=current_year).order_by(order)

  

  
  return render(request,"aboutus.html",{"legislators": current_legislators})


def publicationView(request):
  return render(request,"publications.html",{"request":request})


def publicationListing(request, publication):
  
  resolutions = LegalMeasure.objects.filter(type=str(publication)).order_by('-year','-sequence')
  data = {
    "heading": publication,
    "list": resolutions
  }

  return render(request,"publication-listing.html",{"data":data})



def publicationDetails(request, publication, id, slug):

  try:
    legal_measure = get_object_or_404(LegalMeasure, id=id)
  except Http404:
    return redirect("publication-listing", publication=publication)
  
  related_measures = legal_measure.original_measure.all() | legal_measure.related_measure.all()
  # related_measures_id = []

  # for i in related_measures:
  #   related_measures_id.append(i.legal_measure.id)
  #   related_measures_id.append(i.related_measure.id)

  # related_measures_id = set(related_measures_id)
  
  print(related_measures)

  data = {
    "document": legal_measure,
    "legislators": legal_measure.participations.all(),
    "related_measures": related_measures
  }

  # print(related_measures_id)
 
  return render(request,"publication-details.html",{"data":data})