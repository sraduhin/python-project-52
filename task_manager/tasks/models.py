from django.db import models
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        CustomUser,
        related_name='owner',
        on_delete=models.PROTECT,
        null=True,
    )
    executor = models.ForeignKey(
        CustomUser,
        related_name='executor',
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_('Executor'),
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True,
        verbose_name=_('Status'),
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=_('Labels'),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    
