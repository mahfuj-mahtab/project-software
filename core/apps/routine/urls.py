
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("routine_category/<int:user_id>/", RoutineCategoryView.as_view(),name = 'RoutineCategory'),
    path("routine/<int:user_id>/category/<int:routine_category_id>/", RoutineView.as_view(),name = 'RoutineView'),

]
