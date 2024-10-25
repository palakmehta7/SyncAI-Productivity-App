from django.db import models


STATUSES = (
    ('TODO', 'Todo'),
    ('IN_PROGRESS', 'Inprogress'),
    ('DONE', 'Done'),
)

class Project(models.Model):
    desc = models.CharField(max_length=200)
    start_date = models.DateTimeField("date published")
    summary = models.CharField(max_length=10)
    progress = models.IntegerField(default=0)


class Task(models.Model):
    desc = models.CharField(max_length=200)
    start_date = models.DateTimeField("date published")
    status = models.CharField(max_length=1, choices=STATUSES)
    summary = models.CharField(max_length=10)
    progress = models.IntegerField(default=0)


class Asignee(models.Model):
    name = models.CharField(max_length=200)