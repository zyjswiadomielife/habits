from django.contrib import admin

# Register your models here.
from .models import Goal
from SimpleHabitTracker.models import Habit
from goal_realisation.models import GoalRealisation

admin.site.register(Goal)
admin.site.register(Habit)
admin.site.register(GoalRealisation)