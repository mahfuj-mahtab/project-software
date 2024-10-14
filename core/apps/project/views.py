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
        organizations_data = {
            'my_organizations' : [],
        }
        try:
            user = User.objects.get(id = userId)
        except User.DoesNotExist:
            return Response({'error': 'User not available'},status = status.HTTP_403_FORBIDDEN)
        # checking if i have any organization that i have created
        # organizations = Organization.objects.filter(created_by = user).all()
        # organizations_serializers = OrganizationSerializer(organizations,many = True)
        # organizations_data['my_organizations'].append(organizations_serializers.data)
        # checking if i am employee to users company 
        employee = Employee.objects.filter(user = user)
        employee_serialisers = EmployeeSerializer(employee,many = True)
        return Response({'data' : employee_serialisers.data},status=status.HTTP_200_OK)
class ProjectDepartment(APIView):
    def get(self,request,userId,organizationId):
        try:
            user = User.objects.get(id = userId)
        except User.DoesNotExist:
            return Response({'error': 'User not available'},status = status.HTTP_403_FORBIDDEN)
        try:
            organization = Organization.objects.get(id = organizationId)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not available'},status = status.HTTP_403_FORBIDDEN)
        try:
            employee = Employee.objects.get(user = user,organization = organization)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not available'},status = status.HTTP_403_FORBIDDEN)
        organization_serializer = OrganizationSerializer(organization)
        return Response({'data' : organization_serializer.data},status=status.HTTP_200_OK)