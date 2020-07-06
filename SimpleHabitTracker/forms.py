from django import forms
from Goal.models import Goal
from .models import Habit
from django.forms import ModelForm
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class HabitTrackerSubgoalsForm(forms.ModelForm):
	start_at=forms.DateField(widget=DateInput())
	end_at=forms.DateField(widget=DateInput())
	days = forms.CharField(widget=forms.TextInput(attrs={'v-bind': 'inputProps', 'v-on': 'inputEvents'}))
	
	class Meta:
		model = Habit
		fields = [
		'start_at',
		'end_at',
		'days'
		]
