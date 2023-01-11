from django.db import models
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(CustomUser, related_name='owner', on_delete=models.PROTECT, null=True)
    executor = models.ForeignKey(CustomUser, related_name='executor', on_delete=models.PROTECT, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True)
    labels = models.ManyToManyField(Label)
    created_at = models.DateTimeField(auto_now_add=True)

    
