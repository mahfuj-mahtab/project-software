# Generated by Django 5.1.2 on 2024-10-14 03:49

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0003_project_team"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="role",
        ),
        migrations.CreateModel(
            name="EmployeeRole",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="EmployeeRoleteams",
                        to="project.department",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="EmployeeRoleteams",
                        to="project.organization",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="employee",
            name="role",
            field=models.ManyToManyField(to="project.employeerole"),
        ),
    ]
