from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import GoalCreateForm
from SimpleHabitTracker.forms import HabitTrackerSubgoalsForm
from SimpleHabitTracker.models import Habit
from goal_realisation.models import GoalRealisation
from .models import Goal
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

@login_required
def goal_create_view(request):
	form = GoalCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		method = form.cleaned_data['method']
		if method == 'SIMPLE':
			subgoals_html = 'SimpleHabitTracker:create_simple_subgoal'
		else:
			subgoals_html = 'Goal:create_complex_subgoal' #tutaj dotychczasowy subgoal.html
		return HttpResponseRedirect(reverse(subgoals_html))
	context = {
	'form':form
	}
	return render (request,'Goal/goal_create.html', context)

def complex_subgoal_create_view(request):
	return render (request,"Goal/create_complex_subgoal.html", {})

def simple_goal_detail(request, id):
	user = 	request.user.id
	username = 	request.user.username
	refusal=''
	obj1=get_object_or_404(Goal, id=id)
	progress_slug=obj1.slug+username
	try: 
		obj2=Habit.objects.get(slug=obj1.slug)
	except:
		obj2 = None

	has_joined = obj1.joined.filter(id=user)
	if 'joinbutton' in request.POST:
		try:
			instance=GoalRealisation.objects.get(slug=progress_slug)
			if instance.slug == progress_slug:
				refusal = "true"
		except:
			obj1.joined.add(user)
			obj1.save()
			try:
				instance = GoalRealisation(participant=request.user, slug=progress_slug, remaining_days=obj2.days, progress_record="", title=obj1.title, completed = 0, failed = 0, percentage = 0)
				instance.save()
			except:
				pass
	#po wciśnięciu przycisku "dołącz" następuje sprawdzenie czy bierzący użytkownik rozpoczął już to zadanie. Jeśli nie, to tworzona jest 
	#instancja dla tego użytkownika w tym zadaniu i zostaje dołączony.
	if 'leavebutton' in request.POST:
		obj1.joined.remove(user)
		obj1.save()
	#wyłącznie odłącza użytkownika. Nie ma możliwości ponownego dołączenia.

	days_list=progress(obj1.id, username, obj2, request)
	current_date=datetime.strftime(datetime.date(datetime.now()),'%d.%m.%Y')

	percentage = statistics(progress_slug, obj2)[2]
	completed = statistics(progress_slug, obj2)[0]
	failed = statistics(progress_slug, obj2)[1]

	try:
		instance=GoalRealisation.objects.all()
	except:
		instance = None

	context = {
	'goal_object':obj1,
	'habit_object':obj2,
	'goal_realisation_obj':instance,
	'progress_slug':progress_slug,
	'has_joined':has_joined,
	'days_list':days_list,
	'current_date':current_date,
	'refusal':refusal,
	}
	return render(request, 'Goal/simple_goal_detail.html', context)
	#Widok na utworzony goal z habit trackerem

def progress(goal_id, username, habitobj, request):
	days_list=[]
	progress_record = []
	current_date=datetime.date(datetime.now())
	current_date_string=datetime.strftime(current_date,'%d.%m.%Y')
	try:
		goal=get_object_or_404(Goal, id=goal_id)
		progress_slug=goal.slug+username
		obj=GoalRealisation.objects.get(slug=progress_slug)
		habitobj = Habit.objects.get(slug=goal.slug)
		days=obj.remaining_days
		progress_record = obj.progress_record
		days_list=days.split(",")
		progress_record=progress_record.split(",")		
	except:
		pass
	#pobiera listę dni i listę postępów dla danego użytkownika w danym zadaniu jeśli jest dostępna
	number_of_days=len(days_list)
	try:
		for day in days_list:
			date = datetime.date(datetime.strptime(day, '%d.%m.%Y'))
			print (date, current_date, current_date_string)
			if current_date == date:
				del days_list[:days_list.index(current_date_string)]
				fails = ('0 ')*(number_of_days-len(days_list))
				fails = fails.split()
				progress_record.extend(fails)
				progress_record_str=','.join(progress_record)
				obj.progress_record=progress_record_str
				obj.failed = statistics(progress_slug, habitobj)[1]
				remaining_days=','.join(days_list)		
				obj.remaining_days=remaining_days	
				obj.save()
				print (progress_slug)
	except:
		pass
	#usuwa dni z listy dni do zrobienia jeżeli są starsze niż dzisiejsza data i dodaje 0 do listy postępów za każdy dzień który przepadł

	if 'progressbuton' in request.POST:	
		checkboxes = request.POST.getlist('Check_completed')
		print(statistics(progress_slug, habitobj)[0])
		for day in checkboxes:
			days_list.remove(day)
			progress_record.append('1')
			print(progress_record)
			remaining_days=','.join(days_list)
			progress_record_str=','.join(progress_record)
			obj.remaining_days=remaining_days
			obj.progress_record=progress_record_str
			obj.save()
			obj.completed = statistics(progress_slug, habitobj)[0]
			obj.percentage = int(statistics(progress_slug, habitobj)[2])
			obj.save()
			# print (statistics(progress_record_str))
			if len(days_list)==0:
				user=request.user.id
				goal.joined.remove(user)
				goal.save()
		#jeżeli użytkownik zaznaczy że wykonał zadanie na dany dzień, dzień jest usuwany z listy dni do zaliczenia a w liście postępów dodaje 1
	
	return days_list

def statistics(progress_slug, habit_obj):
	successes = 0
	fails = 0
	percent_of_completion = 0
	try:
		obj = GoalRealisation.objects.get(slug=progress_slug)
		days=habit_obj.days
		statistics=obj.progress_record
		statistics=statistics.split(",")
		days=days.split(",")
		successes = statistics.count('1')
		fails = statistics.count('0')
		percent_of_completion = round(successes/len(days)*100,0)
	except:
		pass
	return successes, fails, percent_of_completion
# funkcja podsumowuje ilość wykonanych dni, ilość nie wykonanych dni i postęp w procentach
def nearest_day(goal_id, username, request):
	nearest_day=''
	try:
		goal=get_object_or_404(Goal, id=goal_id)
		progress_slug=goal.slug+username
		obj=GoalRealisation.objects.get(slug=progress_slug)
		days=obj.remaining_days
		days_list=days.split(",")
		nearest_day = days_list[0]
	except:
		pass
	return nearest_day
	#funkcja do zwracania najbliższego dnia. Jako argumenty przyjmuje id_goala, nazwę użytkownia i request. Jeżeli czegoś brakuje to zwróci pusty string.

class GoalListView(ListView):
	template_name = 'Goal/goals_list.html'
	queryset = Goal.objects.all()
# made by Maciej Faber