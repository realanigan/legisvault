from django import forms
from .models import LegalMeasure
import re

class LegalMeasureForm(forms.ModelForm):
  
  number = forms.CharField(label="Number")

  class Meta:
    model = LegalMeasure
    fields = ["type", "number", "title", "date_approved", "pdf_file"]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    if self.instance.pk:
        self.fields['number'].initial = self.instance.number

  def clean_code(self):
    number = self.cleaned_data['number']

    match = re.match(r"^(?P<year>\d{4})-(?P<num>\d+)(?P<suffix>[A-Za-z]*)$", number)
    if not match:
      raise forms.ValidationError("Format must be YYYY-NN or YYYY-NNA")

    year = int(match.group("year"))
    sequence = int(match.group("num"))   # normalize "01" → 1
    suffix = match.group("suffix").upper() if match.group("suffix") else ""
    
    self.instance.year = year
    self.instance.sequence = sequence
    self.instance.suffix = suffix

    return number
  

  def save(self, commit=True):
    instance = super().save(commit=False)
    instance.year = self.cleaned_data['year']
    instance.number = self.cleaned_data['number']
    if commit:
      instance.save()
    return instance
