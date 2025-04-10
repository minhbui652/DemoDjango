from Utils.models.TimeStampedModel import TimeStampedModel
from django.db import models


class Project(TimeStampedModel):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'Project'

    def __str__(self):
        return self.title
