# Generated by Django 4.1.5 on 2023-01-16 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_alter_task_executor_alter_task_labels_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='Executor'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Name'),
        ),
    ]