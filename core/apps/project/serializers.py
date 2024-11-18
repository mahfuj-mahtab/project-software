from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        depth = 1
class OrganizationSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'
        depth = 1
# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        depth = 1
class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employee
        exclude = ()
        depth = 1

class ProjectTaskSerializer(serializers.ModelSerializer):
    assigned_to = EmployeeSerializer(many=True)
    class Meta:
        model = Task
        fields = '__all__'
        depth = 1
class ProjectTaskListSerializer(serializers.ModelSerializer):
    tasks = ProjectTaskSerializer(many = True)

    class Meta:
        model = TaskList
        fields = '__all__'
        depth = 1
