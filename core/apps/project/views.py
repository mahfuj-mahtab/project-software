from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ProjectOrganization(APIView):
    permission_classes = [IsAuthenticated]

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
            # department = Department(name = 'Administration',organization = organization,created_by = user)
            # department.save()
           
            
            employee = Employee(organization = organization,user = user,role = 'ADMIN',status = 'APPROVED')
            employee.save()
            return Response({'success' : 'Organization Created'},status=status.HTTP_200_OK)
class ProjectDepartment(APIView):
    permission_classes = [IsAuthenticated]

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
    def post(self,request,userId,organizationId):
        data = request.data
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
        if(len(data['department_name']) == 0):
            return Response({'error': 'Department name cannot be empty'},status = status.HTTP_404_NOT_FOUND)
        department = Department(name = data['department_name'],organization = organization,created_by = user)
        department.save()
        return Response({'success' : 'Department Created'},status=status.HTTP_200_OK)

class ProjectProject(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def get(self, request, userId, organizationId):
        user = self.get_object_or_404(User, id=userId)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        employee = self.get_object_or_404(Employee, user=user, organization=organization)
        if not employee:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

       

        # Query optimization with select_related (if applicable)
        projects = Project.objects.filter(organization=organization)

        # Serialize and return project data
        project_serializer = ProjectSerializer(projects, many=True)
        return Response({'data': project_serializer.data}, status=status.HTTP_200_OK)
    def post(self, request, userId, organizationId):
        user = self.get_object_or_404(User, id=userId)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        employee = self.get_object_or_404(Employee, user=user, organization=organization)
        if not employee:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Query optimization with select_related (if applicable)
        data = request.data
        project_name = data['project_name']
        project_description = data['project_description']
        project_deadline = data['project_deadline']
        if(len(data['project_name']) == 0):
            return Response({'error': 'Project name cannot be empty'},status = status.HTTP_404_NOT_FOUND)
        project = Project(name = project_name,description = project_description,deadline = project_deadline,organization = organization,created_by = user)
        project.save()
        project.members.set([employee])
        project.save()
        return Response({'success' : 'Project Created'},status=status.HTTP_200_OK)
class ProjectSingleProject(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def get(self, request, userId, organizationId,projectId):
        user = self.get_object_or_404(User, id=userId)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user)

        if employee:
            # Get all teams that the employee is part of as a list of IDs

            project = self.get_object_or_404(Project, organization=organization,id = projectId)
            if not project:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                if project.members.filter(id=employee[0].id).exists():
                    tasklists = TaskList.objects.filter(project = project)
                    tasklists_serializers = ProjectTaskListSerializer(tasklists,many = True)
                    return Response({'data': tasklists_serializers.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)





        else:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
class ProjectSingleProjectTaskListAdd(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def post(self, request, userId, organizationId,projectId):
        user = self.get_object_or_404(User, id=userId)
        data = request.data
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user)

        if employee:
            # Get all teams that the employee is part of as a list of IDs
            project = self.get_object_or_404(Project, organization=organization,id = projectId)
            if not project:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                if project.members.filter(id=employee[0].id).exists() and (employee[0].role == 'ADMIN' or employee[0].role == 'EDITOR'):
                    name = request.data['name']
                    description = request.data['description']
                    task_status = request.data['status']
                    start_date = request.data['start_date']
                    due_date = request.data['due_date']
                    task_list = TaskList(name = name, description = description,status = task_status,start_date = start_date, due_date = due_date,project = project,created_by = employee[0])
                    task_list.save()
                    return Response({'data': 'Task List Created'}, status=status.HTTP_200_OK)
                    
                else:
                    return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)
class ProjectSingleProjectTaskAdd(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def post(self, request, userId, organizationId,projectId,tl):
        user = self.get_object_or_404(User, id=userId)
        data = request.data
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user)

        if employee:
            # Get all teams that the employee is part of as a list of IDs
            project = self.get_object_or_404(Project, organization=organization,id = projectId)
            if not project:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                if project.members.filter(id=employee[0].id).exists() and (employee[0].role == 'ADMIN' or employee[0].role == 'EDITOR'):
                    task_list = self.get_object_or_404(TaskList,id = tl)
                    if not task_list:
                        return Response({'error': 'TaskList not found'}, status=status.HTTP_404_NOT_FOUND)
                    name = request.data['name']
                    description = request.data['description']
                    priority = request.data['priority']
                    task_status = request.data['status']
                    start_date = request.data['start_date']
                    due_date = request.data['due_date']
                    members = request.data['members']
                    
                    task = Task(title = name, description = description,priority = priority,status = task_status,start_date = start_date, due_date = due_date,task_list = task_list)
                    task.save()
                    if isinstance(members,str):
                        em = Employee.objects.get(id = members)
                        task.assigned_to.add(em)

                    elif(isinstance(members,list)):
                        for member in members:
                            em = Employee.objects.get(id = member)
                            task.assigned_to.add(em)

                    
                    task.save()
                    return Response({'data': 'Task List Created'}, status=status.HTTP_200_OK)
                    
                else:
                    return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)
        

        # Serialize and return project data
class ProjectTeams(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def get(self, request, userId, organizationId):
        user = self.get_object_or_404(User, id=userId)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user)

        if employee:

            # Fetch all employee under the organization and department
            employees = Employee.objects.filter(organization=organization)

            # Iterate over the teams and check if the employee is part of each team
            employees_serializers = EmployeeSerializer(employees, many = True)
            return Response({"data" : employees_serializers.data},status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)


        # Query optimization with select_related (if applicable)
        

        # Serialize and return project data
    def post(self, request, userId, organizationId):
        user = self.get_object_or_404(User, id=userId)
        data = request.data
        team_name = data['team_name']
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user).prefetch_related('team').first()

        if employee:
            # TODO : Employee permission need to check if employee have permission to create or not
            # Fetch all teams under the organization and department
            team = Team(name = team_name,organization = organization,created_by = user)
            team.save()

            # Iterate over the teams and check if the employee is part of each team
            
            return Response({"data" : 'Team created successfully'},status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)


        # Query optimization with select_related (if applicable)
        

        # Serialize and return project data
class ProjectSingleProjectMember(APIView):
    permission_classes = [IsAuthenticated]

    def get_object_or_404(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            return None

    def get(self, request, userId, organizationId,projectId):
        user = self.get_object_or_404(User, id=userId)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user)

        if employee:
            # Get all teams that the employee is part of as a list of IDs
            members = []
            project = self.get_object_or_404(Project, organization=organization,id = projectId)
            if not project:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                if project.members.filter(id=employee[0].id).exists():
                    for mem in project.members.filter():
                        member = {
                            "name" : mem.user.first_name,
                            "email" : mem.user.email,
                            "id" : mem.id,
                            # TODO : NEED TO ADD IMAGE 
                        }
                        members.append(member)
                    
                    return Response({'data': members}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)


        # Query optimization with select_related (if applicable)
        

        # Serialize and return project data
    def post(self, request, userId, organizationId,projectId):
        user = self.get_object_or_404(User, id=userId)
        data = request.data
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        organization = self.get_object_or_404(Organization, id=organizationId)
        if not organization:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)

        # employee = self.get_object_or_404(Employee, user=user, organization=organization)
        # if not employee:
        #     return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        

        # Fetch the employee along with their teams using prefetch_related
        employee = Employee.objects.filter(organization=organization, user=user)

        if employee:
            # Get all teams that the employee is part of as a list of IDs
            members = []
            project = self.get_object_or_404(Project, organization=organization,id = projectId)
            if not project:
                return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                if project.members.filter(id=employee[0].id).exists() and (employee[0].role == 'ADMIN' or employee[0].role == 'EDITOR'):
                    email = request.data['email']
                    role = request.data['role']
                    usr = User.objects.filter(email = email)
                    if(len(usr) == 1):
                        employ = Employee.objects.filter(organization=organization, user=usr[0]).first()
                        if(employ):
                            project.members.add(employ) 
                            project.save()
                            return Response({'data': 'Member Assigned'}, status=status.HTTP_200_OK)


                        else:
                            employee_create = Employee(user = usr[0],organization = organization, role = role, status = 'INVITED')
                            employee_create.save()
                            project.members.add(employee_create)
                            project.save()
                            return Response({'data': 'Member Assigned'}, status=status.HTTP_200_OK)
                        
                    else:
                        return Response({'error': 'Something Went Wrong..'}, status=status.HTTP_404_NOT_FOUND)

                    
                else:
                    return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Access Denied'}, status=status.HTTP_404_NOT_FOUND)


        # Query optimization with select_related (if applicable)
        

        # Serialize and return project data
