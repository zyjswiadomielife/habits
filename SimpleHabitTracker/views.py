from django.shortcuts import render, get_object_or_404
# Create your views here.
from .forms import HabitTrackerSubgoalsForm
from Goal.models import Goal
from .models import Habit
from datetime import timedelta, date
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .serializers import HabitSerializer
from rest_framework import viewsets


def slug_retrieve():
	slug 				= 'slug'
	obj 				= Goal.objects.last()
	slug_for_subgoal	= getattr(obj, slug)
	return slug_for_subgoal
	#Pozyskuje slug wprowadzony w formularzu tworzenia Goal (template Goal_create.html)
def subgoal_period_calculator():
	habit_instance = Habit.objects.last()
	start_at='start_at'
	start_at = getattr(habit_instance, start_at)
	end_at='end_at'
	end_at = getattr(habit_instance, end_at)
	for day in range(int ((end_at - start_at).days)+1):
		yield start_at + timedelta(day)
	# Pozyskuje daty wprowadzone w formularzu i generuje kolejne daty dla generatora listy
def subgoal_period_list_generator():
	all_days_in_range = ""
	all_days_in_range_list=[]
	for single_date in subgoal_period_calculator():
		all_days_in_range+=single_date.strftime("%d.%m.%Y")+","
	all_days_in_range = all_days_in_range[:-1]
	return all_days_in_range
	# Zwraca listę wszystkich dat (dla każdego dnia) w postaci stringa żeby przyjął to jako wartość pod textfield w db



@login_required
def habit_subgoal_create_view(request):
	slug = slug_retrieve()
	obj1=Goal.objects.get(slug=slug)
	#Wydobycie sluga z ostatnio utworzonego goal
	try: 
		habit = get_object_or_404 (Habit, slug=slug)
		form = HabitTrackerSubgoalsForm(request.POST or None, instance=habit)
	except:
		form = HabitTrackerSubgoalsForm(request.POST or None)	
	if form.is_valid():
		form.save()
		obj = Habit.objects.last()
		obj.slug = slug
		obj.days = subgoal_period_list_generator()
		obj.save()
		#Zapisywanie sluga takiego jak w Goal i zapisywanie listy dni jako stringa
		return HttpResponseRedirect(reverse('SimpleHabitTracker:pick_dates'))
	context = {
	'form':form,
	'goal_object':obj1
	}
	return render (request,"SimpleHabitTracker/create_simple_subgoal.html", context)
# made by Maciej Faber
@login_required
def simple_subgoal_pick_days(request):
	slug = slug_retrieve()
	obj1=Goal.objects.get(slug=slug)
	obj2=Habit.objects.get(slug=slug)
	days=obj2.days
	days_list=days.split(",")
	#Wczytuje string z datami z db i przetworza go na listę
	checkboxes = request.POST.getlist('Check')
	if 'streambutton' in request.POST:
		days_list=[]
		for day in checkboxes:
			days_list.append(day)
		all_days_in_range=','.join(days_list)
		obj2.days=all_days_in_range
		obj2.save()
		return HttpResponseRedirect(reverse('Goal:simple_goal_detail',args=(obj1.id,) ))
	#Usuwa niezaznaczone daty i nadpisuje listę dat w db (jako string w TextField)
	context = {
	'days_list':days_list,
	'goal_object':obj1,
	'habit_object':obj2
	}
	return render(request, 'SimpleHabitTracker/simple_subgoal_pick_days.html', context)

def login(request):
	return render(request, 'SimpleHabitTracker/login.html', {})
	#to tylko zwrotka na wypadek próby korzystania z funkcji dla zalogowanych użytkowników przez osoby niezalogowane. Powinno się zastąpić ekranem logowania.

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer