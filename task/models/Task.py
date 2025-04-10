from Utils.ConstantVariables.TaskStatus import TaskStatus
from Utils.models.TimeStampedModel import TimeStampedModel
from django.db import models
from task.models.Project import Project
from user.models.User import User


class Task(TimeStampedModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=TaskStatus.CHOICES, default=TaskStatus.PENDING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Task'

    def __str__(self):
        return self.title
