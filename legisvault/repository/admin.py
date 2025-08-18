from django.contrib import admin
from .models import Legislator
# Register your models here.

@admin.register(Legislator)
class LegislatorAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'portrait')