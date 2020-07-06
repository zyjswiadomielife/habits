from django.urls import path
from .views import (goal_create_view,complex_subgoal_create_view, GoalListView, simple_goal_detail)

app_name = 'Goal'
urlpatterns = [
    path('create/', goal_create_view, name='create_goal'),
    path('complex/', complex_subgoal_create_view, name='create_complex_subgoal'),
    path('',GoalListView.as_view(),name='goals-list' ),
    path('detail/<int:id>', simple_goal_detail, name='simple_goal_detail'),
]