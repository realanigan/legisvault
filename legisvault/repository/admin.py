from django.contrib import admin
from .models import Legislator, LegalMeasure, LegislatorTerm
# Register your models here.



class LegislatorTermAdmin(admin.TabularInline):
  model = LegislatorTerm
  extra = 1
  max_num = 1


class LegislatorAdmin(admin.ModelAdmin):
  inlines = [LegislatorTermAdmin]
  

@admin.register(LegalMeasure)
class LegalMeasureAdmin(admin.ModelAdmin):
  pass



admin.site.register(Legislator, LegislatorAdmin)





