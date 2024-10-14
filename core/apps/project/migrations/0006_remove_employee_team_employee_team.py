# Generated by Django 5.1.2 on 2024-10-14 09:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0005_project_department"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="team",
        ),
        migrations.AddField(
            model_name="employee",
            name="team",
            field=models.ManyToManyField(blank=True, null=True, to="project.team"),
        ),
    ]