from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
class EmployeeSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many = True,source = 'team')
    class Meta:
        model = Employee
        fields = '__all__'
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
class ProjectTaskListSerializer(serializers.ModelSerializer):
    tasks = ProjectTaskSerializer(many = True)
    class Meta:
        model = TaskList
        fields = '__all__'
