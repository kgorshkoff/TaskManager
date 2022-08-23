# Generated by Django 4.1 on 2022-08-23 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=512)),
                ('status', models.CharField(choices=[('New task', 'New'), ('In development', 'In Development'), ('In QA', 'In Qa'), ('In code review', 'In Code Review'), ('Ready for release', 'Ready For Release'), ('Released', 'Released'), ('Archived', 'Archived')], max_length=20)),
                ('priority', models.IntegerField()),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('changed_at', models.DateField()),
                ('finish_until', models.DateField()),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='authored_tasks', to=settings.AUTH_USER_MODEL)),
                ('tag', models.ManyToManyField(to='main.tag')),
            ],
        ),
    ]