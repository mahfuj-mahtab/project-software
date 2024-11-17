
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("organization/fetch/<int:userId>/", ProjectOrganization.as_view(),name = 'project organization'),
    # path("organization/fetch/department/<int:userId>/<str:organizationId>/", ProjectDepartment.as_view(),name = 'project department'),
    path("organization/fetch/project/<int:userId>/<str:organizationId>/", ProjectProject.as_view(),name = 'project project fetch'),
    path("organization/fetch/single/project/<int:userId>/<str:organizationId>/<str:projectId>/", ProjectSingleProject.as_view(),name = 'project single project fetch'),
    path("organization/fetch/members/single/project/<int:userId>/<str:organizationId>/<str:projectId>/", ProjectSingleProjectMember.as_view(),name = 'project single project member  fetch'),
    path("organization/add/single/project/tasklist/<int:userId>/<str:organizationId>/<str:projectId>/", ProjectSingleProjectTaskListAdd.as_view(),name = 'ProjectSingleProjectTaskListAdd '),
    path("organization/add/single/project/task/<int:userId>/<str:organizationId>/<str:projectId>/<str:tl>/", ProjectSingleProjectTaskAdd.as_view(),name = 'ProjectSingleProjectTaskAdd '),
    path("organization/add/single/project/task/<int:userId>/<str:organizationId>/<str:projectId>/<str:tl>/<str:task_id>/", ProjectSingleProjectTaskDetails.as_view(),name = 'ProjectSingleProjectTaskDetails '),
    path("organization/fetch/project/teams/<int:userId>/<str:organizationId>/", ProjectTeams.as_view(),name = 'project ProjectTeams fetch'),
]
