from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
# Create your views here.
class RoutineCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"message":"User Does not exist"},status=status.HTTP_404_NOT_FOUND)
        routine_category = RoutineCategory.objects.filter(user=user)
        serializer = RoutineCategorySerializer(routine_category,many=True)
        return Response({'data' : serializer.data},status=status.HTTP_200_OK)
    def post(self,request,user_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"message":"User Does not exist"},status=status.HTTP_404_NOT_FOUND)
        data = request.data
        routine_category = RoutineCategory.objects.create(user=user,name=data['name'])
        serializer = RoutineCategorySerializer(routine_category)
        return Response({'data':serializer.data},status=status.HTTP_201_CREATED)
    def put(self,request,user_id,routine_category_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"message":"User Does not exist"},status=status.HTTP_404_NOT_FOUND)
        try:
            routine_category = RoutineCategory.objects.get(id=routine_category_id,user = user)
        except:
            return Response({"message":"Routine Category Does not exist"},status=status.HTTP_404_NOT_FOUND)
        data = request.data
        routine_category.name = data['name']
        routine_category.save()
        serializer = RoutineCategorySerializer(routine_category)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
class RoutineView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id,routine_category_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"message":"User Does not exist"},status=status.HTTP_404_NOT_FOUND)
        try:
            routine_category = RoutineCategory.objects.get(id=routine_category_id,user = user)
        except:
            return Response({"message":"Routine Category Does not exist"},status=status.HTTP_404_NOT_FOUND)
        routine = Routine.objects.filter(routine_category=routine_category,user=user)
        serializer = RoutineSerializer(routine,many=True)
        return Response({'data' : serializer.data},status=status.HTTP_200_OK)
    def post(self,request,user_id,routine_category_id):
        try:
            user = User.objects.get(id=user_id)
        except:
            return Response({"message":"User Does not exist"},status=status.HTTP_404_NOT_FOUND)
        try:
            routine_category = RoutineCategory.objects.get(id=routine_category_id,user = user)
        except:
            return Response({"message":"Routine Category Does not exist"},status=status.HTTP_404_NOT_FOUND)
        data = request.data
        routine = Routine.objects.create(user=user,routine_category=routine_category,task=data['task'],start=data['start_time'],end=data['end_time'],day=data['day'],color=data['color'])
        routine.save()

        return Response({'message':'Routine created successfully'},status=status.HTTP_201_CREATED)