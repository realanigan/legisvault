import os
import uuid
from django.db import models
from django.utils.text import slugify


def legal_measure_path(instance, filename):
  return os.path.join('legislative-measures',instance.type, filename)


# Represents the elected Officials and Ex-Oficio of Sangguniang Bayan
class Legislator(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  portrait = models.ImageField(
    upload_to="legislator/portrait", 
    null=True, 
    blank=True, 
    default="static/images/johndoe.png")

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

#This Model represent the terms and position of the legislators. Good for historical Data
class LegislatorTerms(models.Model):
  POSITION_CHOICES = [
    ("councilor", "Municipal Councilor"),
    ("vice_mayor", "Municipal Vice Mayor"),
    ("abc_president", "ABC President"),
    ("ip_representative", "IP Representative"),
    ("sk_federation_president", "SK Municipal Federation President")
  ]

  legislator = models.ForeignKey(Legislator, on_delete=models.CASCADE, related_name="terms")
  position = models.CharField(max_length=150, choices=POSITION_CHOICES)
  start_of_term = models.DateField()
  end_of_term = models.DateField()
  remarks = models.TextField()

#This Model represents the legal documents enacted by the sangguniang bayan
class LegalMeasure(models.Model):
  TYPE_CHOICES = [
    ("resolution", "SB Resolution"),
    ("ordinance", "Ordinance"),
    ("appropriation", "Appropriation Ordinance")
    ]

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  type = models.CharField(max_length=150, choices=TYPE_CHOICES)
  title = models.TextField()
  slug = models.TextField()
  date_approved = models.DateField()
  pdf_file = models.FileField(upload_to=legal_measure_path)
  date_added = models.DateTimeField(auto_now_add=True)

  legislator = models.ManyToManyField(LegislatorTerms, through="Participation" ,related_name="measures")
  related_measures = models.ManyToManyField('self', through='MeasureRelation', through_fields=('legal_measure', 'related_measure'))


  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)

      super().save(*args, **kwargs)


  def __str__(self):
    return self.title

# This model represent the current Committee Present in the Sangguniang Bayan
class Committee(models.Model):
  name = models.CharField(max_length=255, unique=True)
  description = models.TextField()
  slug = models.TextField()

  legislator = models.ManyToManyField(LegislatorTerms, through="CommitteeMembership", related_name="legislators")
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
    ("chairman", "Chairman"),
    ("vice_chairman", "Vice Chairman"),
    ("member", "member")
  ]
  legislator = models.ForeignKey(LegislatorTerms, on_delete=models.CASCADE, related_name="committee_membership")
  committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name="committee")
  role = models.CharField(max_length=100, choices=ROLE_CHOICES)
  start_date = models.DateField()
  end_date = models.DateField()

# This model is the intersecting entity for LegislatorTerms(Legislator) and Enacted Legal Documents
class Participation(models.Model):
  ROLE_CHOICES = [
    ("author", "Author"),
    ("co_author", "Co-Author"),
    ("sponsor", "Sponsor")
  ]
  legal_measure = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="participations")
  legislator_term = models.ForeignKey(LegislatorTerms, on_delete=models.CASCADE, related_name="participations")
  role = models.CharField(max_length=50, choices=ROLE_CHOICES)

# This model is for resolving legal documents relation to itself like 
class MeasureRelation(models.Model):
  RELATION_TYPE_CHOICES = [
    ("amended", "Amended"),
    ("related", "Related")
  ]

  legal_measure = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="original_measure")
  related_measure = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="related_measure")
  relation_type = models.CharField(max_length=20, choices=RELATION_TYPE_CHOICES)
  description = models.TextField(null=True,blank=True)

#This model is fixing multiple committee author/sponsor for enacted legal documents 
class CommitteeMeasure(models.Model):
  ROLE_CHOICES = [
    ("author", "Author"),
    ("co_author", "Co-Author"),
    ("sponsor", "Sponsor")
  ]
  
  legal_measure = models.ForeignKey(LegalMeasure, on_delete=models.CASCADE, related_name="committee_measure")
  committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name="committees")
  role = models.CharField(max_length=50, choices=ROLE_CHOICES)

