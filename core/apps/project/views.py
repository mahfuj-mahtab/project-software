from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
# Create your views here.
class ProjectOrganization(APIView):
    def get(self,request,userId):
        try:
            user = User.objects.get(id = userId)
        except User.DoesNotExist:
            return Response({'error': 'User not available'},status = status.HTTP_403_FORBIDDEN)
        organizations = Organization.objects.filter(created_by = user).all()
        organizations_serializers = OrganizationSerializer(organizations,many = True)
        return Response({'data' : organizations_serializers.data},status=status.HTTP_200_OK)
class ProjectDepartment(APIView):
    def get(self,request,userId,organizationId):
        try:
            user = User.objects.get(id = userId)
        except User.DoesNotExist:
            return Response({'error': 'User not available'},status = status.HTTP_403_FORBIDDEN)
        try:
            organization = Organization.objects.get(id = organizationId,created_by = user)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not available'},status = status.HTTP_403_FORBIDDEN)
        departments = Department.objects.filter(created_by = user,organization = organization).all()
        departments_serializers = OrganizationSerializer(departments,many = True)
        return Response({'data' : departments_serializers.data},status=status.HTTP_200_OK)