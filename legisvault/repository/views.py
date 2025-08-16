from django.shortcuts import render

# Create your views here.
def indexview(request):
  return render(request,"home.html",{"request":request})


def aboutUsView(request):
  return render(request,"aboutus.html",{})


def publicationView(request):
  return render(request,"publication.html",{"request":request})


def publicationSectionView(request):
  return render(request,"publication-section.html",{"request":request})