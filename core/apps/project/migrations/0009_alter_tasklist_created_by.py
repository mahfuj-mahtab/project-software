# Generated by Django 5.1.2 on 2024-11-07 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0008_remove_team_department_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tasklist",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="project.employee"
            ),
        ),
    ]
