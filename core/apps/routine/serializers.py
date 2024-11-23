from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        exclude = ['user']
        depth = 1
class RoutineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineCategory
        exclude = ['user']
        depth = 1