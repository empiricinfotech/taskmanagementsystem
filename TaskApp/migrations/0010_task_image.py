# Generated by Django 4.1.7 on 2023-04-05 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TaskApp", "0009_notification_createddate"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="Image",
            field=models.ImageField(blank=True, null=True, upload_to="taskImage"),
        ),
    ]
