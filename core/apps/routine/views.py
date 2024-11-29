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
        data = {
            
        }
        saturday_routine = Routine.objects.filter(routine_category=routine_category,user=user,day = 'SATURDAY').order_by('start')
        sunday_routine = Routine.objects.filter(routine_category=routine_category,user=user,day = 'SUNDAY').order_by('start')
        monday_routine = Routine.objects.filter(routine_category=routine_category,user=user,day = 'MONDAY').order_by('start')
        tuesday_routine = Routine.objects.filter(routine_category=routine_category,user=user,day = 'TUESDAY').order_by('start')
        wednesday_routine = Routine.objects.filter(routine_category=routine_category,user=user,day = 'WEDNESDAY').order_by('start')
        thursday_routine = Routine.objects.filter(routine_category=routine_category,user=user,day = 'THURSDAY').order_by('start')
        friday_routine = Routine.objects.filter(routine_category=routine_category,user=user,day = 'FRIDAY').order_by('start')
        data['saturday'] = RoutineSerializer(saturday_routine,many = True).data
        data['sunday'] = RoutineSerializer(sunday_routine,many = True).data
        data['monday'] = RoutineSerializer(monday_routine,many = True).data
        data['tuesday'] = RoutineSerializer(tuesday_routine,many = True).data
        data['wednesday'] = RoutineSerializer(wednesday_routine,many = True).data
        data['thursday'] = RoutineSerializer(thursday_routine,many = True).data
        data['friday'] = RoutineSerializer(friday_routine,many = True).data









        # serializer = RoutineSerializer(routine,many=True)
        return Response({'data' : data},status=status.HTTP_200_OK)
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