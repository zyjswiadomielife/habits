from django.db import models
from tinymce import models as tinymce_models
from django.contrib.contenttypes.fields import GenericRelation
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User

# Create your models here.
class Goal(models.Model):
	SIMPLE_COMPLEX = (
		("SIMPLE", "Simple"),
		("COMPLEX", "Complex"),
		)
	title = models.CharField(max_length=255, verbose_name='Tytuł', unique=True)
	image = models.ImageField(blank=True, verbose_name='Tło')
	body = tinymce_models.HTMLField(verbose_name='Treść')
	#votes = GenericRelation(LikeDislike, related_query_name='goalvotes')
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	slug = AutoSlugField(populate_from='title')
	joined = models.ManyToManyField(User, related_name='joinedtogoal', blank=True)
	method = models.CharField(max_length=7, choices=SIMPLE_COMPLEX, default="COMPLEX")

	def get_absolute_url(self):
		return f"/detail/{self.id}"
