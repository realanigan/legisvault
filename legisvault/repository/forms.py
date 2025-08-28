from django import forms
from .models import LegalMeasure
import re
from datetime import datetime

class LegalMeasureForm(forms.ModelForm):
  
  number = forms.CharField(label="Number")

  class Meta:
    model = LegalMeasure
    fields = ["type", "number", "title", "date_approved", "pdf_file"]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    if self.instance.pk:
      self.fields['number'].initial = self.instance.number


  def get_initial_for_field(self, field, field_name):
        if field_name == "number" and not self.instance.pk:
            return f"{datetime.now().year}-"
        return super().get_initial_for_field(field, field_name)


  def clean_number(self):
    number = self.cleaned_data['number']

    match = re.match(r"^(?P<year>\d{4})-(?P<num>\d{1,4})(?P<suffix>[A-Z]*)$", number, re.IGNORECASE)
    if not match:
      raise forms.ValidationError(("Format must be YYYY-NN or YYYY-NNA (e.g. 2025-01 or 2025-15A)"), code="invalid")

   
    year = int(match.group("year"))
    sequence = int(match.group("num"))   # normalize "01" → 1
    suffix = match.group("suffix").upper() if match.group("suffix") else ""
  
    self.instance.year = year
    self.instance.sequence = sequence
    self.instance.suffix = suffix
  

    return number
  

  def save(self, commit=True):

    instance = super().save(commit=False)
    if commit:
      instance.save()
    return instance
