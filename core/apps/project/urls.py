
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("organization/fetch/<int:userId>/", ProjectOrganization.as_view(),name = 'project organization'),
    path("organization/fetch/department/<int:userId>/<str:organizationId>/", ProjectDepartment.as_view(),name = 'project department'),
]
