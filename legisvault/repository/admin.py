from django.contrib import admin
from django import forms
from .util import generate_resolution_number
from django.utils.text import slugify
from .forms import LegalMeasureForm

from .models import Legislator, LegalMeasure, LegislatorTerm, Participation, MeasureRelation
# Register your models here.




class LegislatorTermTabular(admin.TabularInline):
  model = LegislatorTerm
  extra = 1
  max_num = 1



@admin.register(Legislator)
class HiddenLegislatorAdmin(admin.ModelAdmin):
    search_fields = ["name"]  # autocomplete needs this

    def name(self, obj):
      return f"{obj.first_name} {obj.last_name}"

    def get_model_perms(self, request):
        """
        Return empty perms dict → hides Legislator from sidebar
        but still keeps it registered for autocomplete.
        """
        return {}
  
@admin.register(LegislatorTerm)
class LegislatorTermAdmin(admin.ModelAdmin):
  
  list_display = ["name", "position", "start_of_term", "end_of_term"]
  autocomplete_fields = ["legislator"]
  list_filter = ["start_of_term"]

  def name(self, obj):
    return f"{obj.legislator.first_name} {obj.legislator.last_name}"



class ParticipationInline(admin.StackedInline):
  model = Participation
  extra = 1  # number of empty rows



class RelatedMeasureInline(admin.StackedInline):
  model = MeasureRelation
  fk_name = "related_measure"
  extra = 1 

@admin.register(LegalMeasure)
class LegalMeasureAdmin(admin.ModelAdmin):
  form = LegalMeasureForm
  inlines = [ParticipationInline, RelatedMeasureInline]
  list_display = ["id", "type", "number", "slug", "title", "date_approved", "pdf_file"]
  ordering = ("-year", "-sequence", "suffix")
  
  # def get_changeform_initial_data(self, request):
  #   return {"number": generate_resolution_number()}
  
@admin.register(MeasureRelation)
class MeasureRelationAdmin(admin.ModelAdmin):
  pass