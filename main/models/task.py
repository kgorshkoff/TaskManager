from django.db import models
from django.utils import timezone

from .status import Status
from .tag import Tag


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=512)
    status = models.CharField(choices=Status.choices, max_length=20)
    priority = models.IntegerField(null=True)

    created_at = models.DateTimeField(default=timezone.now)
    start_at = models.DateTimeField(null=True)
    finish_until = models.DateTimeField(null=True)

    tag = models.ManyToManyField(Tag)

    author = models.ForeignKey(
        "User", related_name="authored_tasks", on_delete=models.DO_NOTHING, null=True
    )
    assignee = models.ForeignKey(
        "User", related_name="assigned_tasks", on_delete=models.DO_NOTHING, null=True
    )

    def __str__(self):
        return f"[{self.id}] {self.title}"
