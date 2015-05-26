from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
	title = models.CharField(max_length=64)
	summary = models.CharField(max_length=256, blank=True, null=True)
	content = models.TextField()
	view_count = models.IntegerField(blank=True, null=True)
	ranking = models.IntegerField(blank=True, null=True)
	created_at = models.DateTimeField()
	updated_at = models.DateTimeField()
	category_name = models.ForeignKey("Category")
	#author = models.ForeignKey()

	def __unicode__(self):
		return self.title

class Comment(models.Model):
	pass

class Category(models.Model):
	name = models.CharField(max_length=32, unique=True)

	def __unicode__(self):
		return self.name
