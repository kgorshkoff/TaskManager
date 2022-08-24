# Generated by Django 4.1 on 2022-08-23 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_tag_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="changed_at",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="task",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="task",
            name="finish_until",
            field=models.DateTimeField(),
        ),
    ]
