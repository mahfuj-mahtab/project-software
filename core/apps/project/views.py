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
    def post(self,request,userId):
        try:
            user = User.objects.get(id = userId)
        except User.DoesNotExist:
            return Response({'error': 'User not available'},status = status.HTTP_403_FORBIDDEN)

        data = request.data
        if(len(data['organization_name']) == 0):
            return Response({'error': 'Ornagization name cannot be empty'},status = status.HTTP_404_NOT_FOUND)
        else:
            organization = Organization(name = data['organization_name'], created_by = user)
            organization.save()
            department = Department(name = 'Administration',organization = organization,created_by = user)
            department.save()
            team = Team(name = 'Administration',organization = organization,created_by = user,department = department)
            team.save()
            employeerole = EmployeeRole(name = 'Administration',organization = organization,department = department)
            employeerole.save()
            employee = Employee(organization = organization,user = user)
            employee.save()
            employee.team.set([team])
            employee.role.set([employeerole])
            employee.save()
            return Response({'success' : 'Organization Created'},status=status.HTTP_200_OK)
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
class ProjectProject(APIView):
    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def get(self, request, userId, organizationId, departmentId):
        user = self.get_object_or_404(User, id=userId)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        employee = self.get_object_or_404(Employee, user=user, organization=organization)
        if not employee:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        department = self.get_object_or_404(Department, organization=organization, id=departmentId)
        if not department:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

        # Query optimization with select_related (if applicable)
        projects = Project.objects.filter(organization=organization, department=department)

        # Serialize and return project data
        project_serializer = ProjectSerializer(projects, many=True)
        return Response({'data': project_serializer.data}, status=status.HTTP_200_OK)
class ProjectSingleProject(APIView):
    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def get(self, request, userId, organizationId, departmentId,projectId):
        user = self.get_object_or_404(User, id=userId)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        department = self.get_object_or_404(Department, organization=organization, id=departmentId)
        if not department:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user).prefetch_related('team').first()

        if employee:
            # Get all teams that the employee is part of as a list of IDs
            employee_team_ids = employee.team.values_list('id', flat=True)

            # Fetch all teams under the organization and department
            teams = Team.objects.filter(organization=organization, department=department)

            # Iterate over the teams and check if the employee is part of each team
            for team in teams:
                if team.id in employee_team_ids:
                    project = self.get_object_or_404(Project, organization=organization, department=department,team = team,id = projectId)
                    if not project:
                        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
                    tasklists = TaskList.objects.filter(project = project)
                    tasklists_serializers = ProjectTaskListSerializer(tasklists,many = True)
                    return Response({'data': tasklists_serializers.data}, status=status.HTTP_200_OK)

                else:
                    return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)


        # Query optimization with select_related (if applicable)
        

        # Serialize and return project data
