from django.shortcuts import render, get_object_or_404, redirect
from .models import LegislatorTerm, LegalMeasure, CommitteeMeasure, Legislator, SBProfile
from django.http import Http404, JsonResponse
from datetime import date
from django.db.models import Q, Case, When, IntegerField


## Custom sort (VM, councilor, etc) for database query result
## Helper function for sorting
order = Case(
    When(position='Municipal Vice Mayor', then=1),
    When(position='Municipal Councilor', then=2),
    When(position='ABC President', then=3),
    When(position='IP Representative', then=4),
    When(position='SK Municipal Federation President', then=5),
    default=99,  # everything else goes last
    output_field=IntegerField(),
)


def indexview(request):
  publications = LegalMeasure.objects.order_by("-date_added")[:3]
  profile = SBProfile.objects.get(id=1)


  data = {
    "latest_publications":publications,
    "profile":profile
  }

  return render(request,"home.html", data)


def aboutUsView(request):
  current_year = date.today().year
  current_legislators = LegislatorTerm.objects.filter(start_of_term__year=current_year).order_by(order)
  profile = SBProfile.objects.get(id=1)

  data = {
    "legislators": current_legislators,
    "profile":profile 
  }

  return render(request,"aboutus.html", data)


def publicationView(request):
  profile = SBProfile.objects.get(id=1)

  data = {
      "profile":profile 
    }
  return render(request,"publications.html", data)


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
  
  # Retrieve all measures connected to this measure, in both forward (source→target) and backward (target→source) direction
  related_measures = LegalMeasure.objects.filter(Q(as_source__target=legal_measure) | Q(as_target__source=legal_measure)).exclude(id=legal_measure.id).order_by("-year", "-sequence")

  committees = CommitteeMeasure.objects.filter(legal_measure=legal_measure)

  data = {
    "document": legal_measure,
    "legislators": legal_measure.participations.all(),
    "related_measures": related_measures,
    "committees": committees
  }
 
  return render(request,"publication-details.html",{"data":data})


def getCouncellor(request, id):

  legislator = Legislator.objects.get(id=id)
  data = {
    "name": str(legislator),
    "bio": legislator.biography,

  }


  return JsonResponse(data)
  