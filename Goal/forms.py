from django import forms
from .models import Goal


class GoalCreateForm(forms.ModelForm):

	class Meta:
		model = Goal
		fields = [
		'title',
		'image',
		'body',
		'author',
		'method',
		]
# class GoalForm(forms.Form):
# 	title	= forms.CharField(max_length=255, verbose_name='Tytuł')
# 	image	= forms.ImageField(blank=True, verbose_name='Tło')
# 	body	= tinymce_forms.HTMLField(verbose_name='Treść')
# 	author	= forms.ForeignKey(User, on_delete=models.CASCADE)
# 	method	= forms.CharField(max_length=7, default="COMPLEX")
