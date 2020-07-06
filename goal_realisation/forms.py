from django import forms
from .models import GoalRealisation


class GoalRealisation(forms.ModelForm):

	class Meta:
		model = GoalRealisation
		fields = [
		'title',
		'image',
		'body',
		'author',
		'method',
		]