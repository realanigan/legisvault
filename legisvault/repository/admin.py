from django.contrib import admin
from django import forms
from .util import generate_resolution_number
from django.utils.text import slugify
from .forms import LegalMeasureForm
from datetime import datetime
from .models import Legislator, LegalMeasure, LegislatorTerm, Participation, MeasureRelation



class LegislatorTermInline(admin.StackedInline):
  model = LegislatorTerm
  extra = 0

  
  def get_queryset(self, request):
      queryset = super().get_queryset(request)
      # Filter to show only the most recent book based on 'created_at'
      return queryset.filter(start_of_term__year=2025).order_by('start_of_term')
  
  can_delete = False
  fields = ['position', 'start_of_term', 'end_of_term']  # Specify the fields

  def get_readonly_fields(self, request, obj=None):
      # If obj is None, it's a new object; else, it's an existing object.
      if obj:
          # Fields will be read-only if we're editing an existing object
          return self.fields  # Return all fields as read-only for existing objects
      return []  # No read-only fields when creating a new object
  

@admin.register(Legislator)
class LegislatorAdmin(admin.ModelAdmin):
  inlines = [LegislatorTermInline]
  search_fields = ["name"]  # autocomplete needs this
  list_display = ["name", "current_position", "current_term"]
  

  def current_term(self, obj):
    current_year = 2025
    # Assuming `terms` is a related field on your model, and `start_of_term` is a DateField or DateTimeField
    terms_in_current_year = obj.terms.filter(start_of_term__year=current_year)
    
    # If there are multiple terms, you can format the result, or just return the first one
    # For example, if you want the name of the term:
    if terms_in_current_year.exists():
        # You can customize this to display something else, like a term name or other attribute
        return ', '.join(str(term.start_of_term) for term in terms_in_current_year)
    else:
        return "No terms found"
    
  def current_position(self, obj):
    current_year = datetime.now().year
    # Assuming `terms` is a related field on your model, and `start_of_term` is a DateField or DateTimeField
    position_in_current_year = obj.terms.filter(start_of_term__year=current_year)
    
    # If there are multiple terms, you can format the result, or just return the first one
    # For example, if you want the name of the term:
    if position_in_current_year.exists():
        # You can customize this to display something else, like a term name or other attribute
        return ', '.join(str(term.position) for term in position_in_current_year)
    else:
        return "No terms found"
    

    current_term.admin_order_field = 'current_term_year'  # Make this field sortable
    current_term.short_description = 'Current Term'
    
  def name(self, obj):
    return f"{obj.first_name} {obj.last_name}"

    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict → hides Legislator from sidebar
    #     but still keeps it registered for autocomplete.
    #     """
    #     return {}

  can_delete = False
  
  def has_delete_permission(self, request, obj=None):
    # Prevent deletion of Author instance
    return False  # This disables the delete option in the admin for Author
  


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
  fields = ["type", "number", "title", "date_approved", "pdf_file"]
  list_display = ["id", "type", "number", "slug", "title", "date_approved", "pdf_file"]
  ordering = ("-year", "-sequence", "suffix")
  
  # def get_changeform_initial_data(self, request):
  #   initial = super().get_changeform_initial_data(request)
  #   initial.setdefault("number", f"{datetime.now().year}-")
  #   return initial

  # def get_changeform_initial_data(self, request):
  #   return {"number": generate_resolution_number()}
  
@admin.register(MeasureRelation)
class MeasureRelationAdmin(admin.ModelAdmin):
  pass