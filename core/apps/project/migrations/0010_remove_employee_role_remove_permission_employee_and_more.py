# Generated by Django 5.1.2 on 2024-11-08 03:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0009_alter_tasklist_created_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="employee",
            name="role",
        ),
        migrations.RemoveField(
            model_name="permission",
            name="employee",
        ),
        migrations.RemoveField(
            model_name="permission",
            name="organization",
        ),
        migrations.RemoveField(
            model_name="team",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="team",
            name="organization",
        ),
        migrations.RemoveField(
            model_name="project",
            name="team",
        ),
        migrations.RemoveField(
            model_name="employee",
            name="team",
        ),
        migrations.AddField(
            model_name="employee",
            name="status",
            field=models.TextField(
                choices=[
                    ("INVITED", "INVITED"),
                    ("APPROVED", "APPROVED"),
                    ("PENDING", "PENDING"),
                    ("BANNED", "BANNED"),
                    ("DELETED", "DELETED"),
                ],
                default="INVITED",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="members",
            field=models.ManyToManyField(
                related_name="project_members", to="project.employee"
            ),
        ),
        migrations.DeleteModel(
            name="EmployeeRole",
        ),
        migrations.AddField(
            model_name="employee",
            name="role",
            field=models.TextField(
                choices=[
                    ("ADMIN", "ADMIN"),
                    ("EDITOR", "EDITOR"),
                    ("COMMENTER", "COMMENTER"),
                    ("VIEWER", "VIEWER"),
                ],
                default="VIEWER",
            ),
        ),
        migrations.DeleteModel(
            name="Permission",
        ),
        migrations.DeleteModel(
            name="Team",
        ),
    ]
