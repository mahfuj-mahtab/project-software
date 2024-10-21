
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("organization/fetch/<int:userId>/", ProjectOrganization.as_view(),name = 'project organization'),
    path("organization/fetch/department/<int:userId>/<str:organizationId>/", ProjectDepartment.as_view(),name = 'project department'),
    path("organization/fetch/project/<int:userId>/<str:organizationId>/<str:departmentId>/", ProjectProject.as_view(),name = 'project project fetch'),
    path("organization/fetch/single/project/<int:userId>/<str:organizationId>/<str:departmentId>/<str:projectId>/", ProjectSingleProject.as_view(),name = 'project single project fetch'),
    path("organization/fetch/project/teams/<int:userId>/<str:organizationId>/<str:departmentId>/", ProjectTeams.as_view(),name = 'project ProjectTeams fetch'),
]
