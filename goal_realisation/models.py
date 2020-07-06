from django.db import models
from django.contrib.auth.models import User
from Goal.models import Goal

# Create your models here.
class GoalRealisation(models.Model):
	participant 	= models.ForeignKey(User, on_delete=models.CASCADE)
	title 			= models.CharField(max_length=255, verbose_name='Tytuł')
	slug 			= models.SlugField(max_length=255, unique=True)
	remaining_days	= models.TextField(default="")
	progress_record	= models.TextField(default="")
	completed	= models.IntegerField(default=0)
	failed	= models.IntegerField(default=0)
	percentage	= models.IntegerField(default=0)
