from django.db import models

from django.contrib.auth.models import User
import uuid


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organizations")

    def __str__(self):
        return self.name


# class Department(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="departments")
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.name


# class Team(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="teams")
#     # department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="teams")
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
#     def __str__(self):
#         return self.name
# class EmployeeRole(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="EmployeeRoleteams")
#     # department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="EmployeeRoleteams")

#     def __str__(self):
#         return self.name


class Employee(models.Model):
    ROLE = [
        ('ADMIN', 'ADMIN'),
        ('EDITOR', 'EDITOR'),
        ('COMMENTER', 'COMMENTER'),
        ('VIEWER', 'VIEWER'),

    ]
    STATUS = [
        ('INVITED', 'INVITED'),
        ('APPROVED', 'APPROVED'),
        ('PENDING', 'PENDING'),
        ('BANNED', 'BANNED'),
        ('DELETED', 'DELETED'),

    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_profile")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="employees")
    role = models.TextField(choices=ROLE,default='VIEWER')
    status = models.TextField(choices=STATUS,default = 'INVITED')

    def __str__(self):
        return f"{self.user.first_name} - {self.organization.name}"



class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="projects")
    # department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="department",null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects")
    members = models.ManyToManyField(Employee,related_name="project_members")


class TaskList(models.Model):
    STATUS_CHOICES = [
    # General Project Statuses
    ('Active', 'Active'),
    ('InProgress', 'In Progress'),
    ('OnTrack', 'On Track'),
    ('Delayed', 'Delayed'),
    ('Testing', 'Testing'),
    ('OnHold', 'On Hold'),
    ('Approved', 'Approved'),
    ('Canceled', 'Canceled'),
    ('Planning', 'Planning'),
    ('Completed', 'Completed'),
    ('Closed', 'Closed'),
    
    # Content Creation Specific
    ('Draft', 'Draft'),
    ('Ideation', 'Ideation'),
    ('Editing', 'Editing'),
    ('Publishing', 'Publishing'),
    ('Published', 'Published'),
    ('Scheduled', 'Scheduled'),
    ('Archived', 'Archived'),
    ('Reviewing', 'Reviewing'),
    
    # Marketing & Campaigns
    ('Designing', 'Designing'),
    ('Executing', 'Executing'),
    ('Analyzing', 'Analyzing'),
    ('Optimization', 'Optimization'),
    ('Launch', 'Launch'),
    ('Feedback', 'Feedback'),
    
    # Software Development
    ('Development', 'Development'),
    ('Deployment', 'Deployment'),
    ('BugFixing', 'Bug Fixing'),
    ('CodeReview', 'Code Review'),
    ('Maintenance', 'Maintenance'),
    ('Rollback', 'Rollback'),
    
    # Team Collaboration
    ('Brainstorming', 'Brainstorming'),
    ('AwaitingFeedback', 'Awaiting Feedback'),
    ('Revising', 'Revising'),
    ('ApprovedByTeam', 'Approved by Team'),
    ('FinalReview', 'Final Review'),
    
    # Others
    ('Rescheduled', 'Rescheduled'),
    ('UnderDiscussion', 'Under Discussion'),
    ('Paused', 'Paused'),
    ('Abandoned', 'Abandoned'),
]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="task_lists")
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('InProgress', 'InProgress'),
        ('OnTrack', 'OnTrack'),
        ('Delayed', 'Delayed'),
        ('Testing', 'Testing'),
        ('OnHold', 'OnHold'),
        ('Approved', 'Approved'),
        ('Canceled', 'Canceled'),
        ('Planning', 'Planning'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES,default='Low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ManyToManyField(Employee, related_name="assigned_tasks",blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)


class SingleTask(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('InProgress', 'InProgress'),
        ('OnTrack', 'OnTrack'),
        ('Delayed', 'Delayed'),
        ('Testing', 'Testing'),
        ('OnHold', 'OnHold'),
        ('Approved', 'Approved'),
        ('Canceled', 'Canceled'),
        ('Planning', 'Planning'),
        ('Completed', 'Completed'),
        ('Closed', 'Closed'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES,default='Low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks",blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="files")
