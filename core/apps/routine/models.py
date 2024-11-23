from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RoutineCategory(models.Model):
    name = models.TextField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
class Routine(models.Model):
    DAY = [
        ('SATURDAY' , 'SATURDAY'),
        ('SUNDAY' , 'SUNDAY'),
        ('MONDAY' , 'MONDAY'),
        ('TUESDAY' , 'TUESDAY'),
        ('WEDNESDAY' , 'WEDNESDAY'),
        ('THURSDAY' , 'THURSDAY'),
        ('FRIDAY' , 'FRIDAY'),
    ]
    task = models.TextField(max_length=50)
    start = models.TimeField()
    end = models.TimeField()
    day = models.TextField(choices=DAY)
    color = models.TextField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    routine_category = models.ForeignKey(RoutineCategory,on_delete=models.CASCADE)
