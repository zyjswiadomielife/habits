from django.urls import path, include
from .views import (habit_subgoal_create_view, simple_subgoal_pick_days, login, HabitViewSet)
from rest_framework import routers
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'habits', HabitViewSet)

app_name = 'SimpleHabitTracker'
urlpatterns = [
    path('simple/', habit_subgoal_create_view, name='create_simple_subgoal'),
    path('daypick/', simple_subgoal_pick_days, name='pick_dates'),
    #api
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', login, name='login'),
    path('testdays/', TemplateView.as_view(template_name="SimpleHabitTracker/savedays.html"))
]