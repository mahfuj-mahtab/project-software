# Generated by Django 5.1.2 on 2024-10-13 10:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0002_remove_task_assigned_to_task_assigned_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="team",
            field=models.ManyToManyField(
                related_name="created_team_projects", to="project.team"
            ),
        ),
    ]
