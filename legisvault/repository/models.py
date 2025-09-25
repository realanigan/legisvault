import os
import uuid
from django.db import models
from datetime import date
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


## Defining the path where the pdf file of legal measure will be stored
def legal_measure_path(instance, filename):
  new_file_name = f"{instance.type} No. {instance.number}.pdf"
  return os.path.join('legislative-measures',instance.type + "s", new_file_name)

## Defining the path where the profile picture will be stored
def profile_picture_path(instance, filename):
  folder = str(instance.first_name) + str(instance.last_name)
  return os.path.join('legislator', folder, filename)

# Represents the elected Officials and Ex-Oficio of Sangguniang Bayan
class Legislator(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  portrait = models.ImageField(
    upload_to=profile_picture_path, 
    null=True, 
    blank=True, 
  )
  biography = CKEditor5Field('Content', config_name='default', null=True, blank="True")

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

#This Model represent the terms and position of the legislators. Good for historical Data
class LegislatorTerm(models.Model):
  POSITION_CHOICES = [
    ("Municipal Councilor", "Municipal Councilor"),
    ("Municipal Vice Mayor", "Municipal Vice Mayor"),
    ("ABC President", "ABC President"),
    ("IP Representative", "IP Representative"),
    ("SK Municipal Federation President", "SK Municipal Federation President")
  ]

  legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE, related_name="terms")
  position = models.CharField(max_length=150, choices=POSITION_CHOICES)
  start_of_term = models.DateField()
  end_of_term = models.DateField()
  remarks = models.TextField(null=True, blank=True)

  def __str__(self):
    return f"{self.legislator.first_name} {self.legislator.last_name} - {self.position} ({self.start_of_term.year} - {self.end_of_term.year})"

  class Meta:
    verbose_name = "Legislator Term"
    verbose_name_plural = "Legislator Terms"

#This Model represents the legal documents enacted by the sangguniang bayan
class LegalMeasure(models.Model):
  TYPE_CHOICES = [
    ("SB Resolution", "SB Resolution"),
    ("Municipal Ordinance", "Municipal Ordinance"),
    ("Appropriation Ordinance", "Appropriation Ordinance")
  ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  type = models.CharField(max_length=150, choices=TYPE_CHOICES)
  year = models.IntegerField(null=True, blank=True)
  sequence = models.IntegerField(null=True, blank=True)
  suffix = models.CharField(max_length=5, blank=True)
  title = models.TextField()
  slug = models.TextField()
  date_approved = models.DateField()
  pdf_file = models.FileField(upload_to=legal_measure_path)
  date_added = models.DateTimeField(auto_now_add=True)

  legislator = models.ManyToManyField(LegislatorTerm, through="Participation", related_name="measures")
  related_measures = models.ManyToManyField('self', through='MeasureRelation', through_fields=('source', 'target'), blank=True)


  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)

    super().save(*args, **kwargs)


  @property
  def number(self):
    if self.year is None or self.sequence is None:
      return ""
    
    return f"{self.year}-{self.sequence:02d}{self.suffix}"

  def __str__(self):
    return f"{self.type} No. {self.number}"
  
  class Meta:
    verbose_name = "Legal Measure"

  

# This model represent the current Committee Present in the Sangguniang Bayan
class Committee(models.Model):
  name = models.CharField(max_length=255, unique=True)
  description = models.TextField()
  slug = models.TextField()

  legislator = models.ManyToManyField(LegislatorTerm, through="CommitteeMembership", related_name="legislators")
  legal_measure = models.ManyToManyField(LegalMeasure, through="CommitteeMeasure", related_name="measures")

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)

      super().save(*args, **kwargs)

  def __str__(self):
    return self.name

# This model is an intersecting entity for Legislator and Committee
class CommitteeMembership(models.Model):
  ROLE_CHOICES = [
    ("Chairman", "Chairman"),
    ("Vice Chairman", "Vice Chairman"),
    ("Member", "member")
  ]
  legislator = models.ForeignKey(LegislatorTerm, on_delete=models.CASCADE, related_name="committee_membership")
  committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name="committee")
  role = models.CharField(max_length=100, choices=ROLE_CHOICES)
  start_date = models.DateField()
  end_date = models.DateField()

# This model is the intersecting entity for LegislatorTerms(Legislator) and Enacted Legal Documents
class Participation(models.Model):
  ROLE_CHOICES = [
    ("Author", "Author"),
    ("Co-Author", "Co-Author"),
    ("Sponsor", "Sponsor")
  ]
  legal_measure = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="participations")
  legislator = models.ForeignKey(LegislatorTerm, on_delete=models.CASCADE, related_name="participations")
  role = models.CharField(max_length=50, choices=ROLE_CHOICES)

  class Meta:
    constraints = [
    models.UniqueConstraint(
        fields=["legislator", "legal_measure", "role"],
        name="unique_legislator_measure_role"
    )
  ]

    

# This model is for resolving legal documents relation to itself like 
class MeasureRelation(models.Model):
  RELATION_TYPE_CHOICES = [
    ("amended", "Amended"),
    ("related", "Related")
  ]

  source = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="as_source", verbose_name="Original Measure")
  target = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="as_target", verbose_name="Related Measure")
  relation_type = models.CharField(max_length=20, choices=RELATION_TYPE_CHOICES)
  description = models.TextField(null=True,blank=True)


  def __str__(self):
    return f"{self.target} {self.relation_type} {self.source}"

#This model is fixing multiple committee author/sponsor for enacted legal documents 
class CommitteeMeasure(models.Model):
  ROLE_CHOICES = [
    ("Author", "Author"),
    ("Co-Author", "Co-Author"),
    ("Sponsor", "Sponsor")
  ]
  
  legal_measure = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="committee_measure")
  committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name="committees")
  role = models.CharField(max_length=50, choices=ROLE_CHOICES)


class SBProfile(models.Model):
  name = models.CharField(max_length=250, null=True, blank="True")
  address = models.CharField(max_length=200, null=True, blank="True")
  municipality = models.CharField(max_length=100, null=True, blank="True")
  province = models.CharField(max_length=100, null=True, blank="True")
  short_mandate = CKEditor5Field('Short Mandate', config_name='default', null=True, blank="True")
  mandate = CKEditor5Field('Mandate', config_name='default', null=True, blank="True")
  publication_header = models.CharField(max_length=200, null=True, blank="True")
  publication_description = CKEditor5Field('Publication description', config_name='default', null=True, blank="True")
  vision = CKEditor5Field('Vision', config_name='default', null=True, blank="True")
  mission = CKEditor5Field('Mission', config_name='default', null=True, blank="True")

  class Meta:
    verbose_name = "Profile"