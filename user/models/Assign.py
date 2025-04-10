from Utils.models.TimeStampedModel import TimeStampedModel
from django.db import models
from task.models.Project import Project
from user.models.User import User


class Assign(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    isDeleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'Assign'

    def __str__(self):
        return f'{self.user} - {self.project}'
