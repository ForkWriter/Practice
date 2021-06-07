"""
Definition of models.
"""

from django.db import models
from django.contrib.postgres.fields import ArrayField

class workers(models.Model):
    fam = models.CharField(max_length = 20,blank=True)
    name = models.CharField(max_length = 20, blank=True)
    otch = models.CharField(max_length = 20)
    sex = models.CharField(max_length = 20)
    date = models.DateField(blank=True)
    adres = models.CharField(max_length = 60, blank=True)
    ed = models.CharField(max_length = 20, blank=True)
    school = models.CharField(max_length = 40, blank=True)
    spec = models.CharField(max_length = 20, blank=True,null=True)
    stage = models.IntegerField(blank=True)
    add_abil = models.CharField(max_length = 255)
    reasons = models.CharField(max_length = 255)

class spec(models.Model):
	name = models.CharField(max_length=20)
	conditions=ArrayField(models.CharField(max_length=100))
	price=models.IntegerField()
	id_spec=models.IntegerField()
	id= models.IntegerField(primary_key=True)

class company(models.Model):
	name = models.CharField(max_length=20)
	adres = models.CharField(max_length = 60)
	spec_id = ArrayField(models.IntegerField())

class empl(models.Model):
	person_id=models.IntegerField()
	spec_id=ArrayField(models.IntegerField())
