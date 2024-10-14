from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Employee)
admin.site.register(Permission)
admin.site.register(Project)
admin.site.register(TaskList)
admin.site.register(Task)
admin.site.register(SingleTask)
admin.site.register(Comment)
admin.site.register(File)
admin.site.register(EmployeeRole)