from django.db import models
from Goal.models import Goal
from django.contrib.postgres.fields import JSONField

class Habit(models.Model):
	start_at = 		models.DateField(auto_now=False, auto_now_add=False, verbose_name="Początek", blank=True, null=True)
	end_at = 		models.DateField(auto_now=False, auto_now_add=False, verbose_name="Koniec", blank=True, null=True)
	slug = 			models.SlugField(max_length=255,)
	days = 			models.TextField(default="")

