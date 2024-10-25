from django.db import models


STATUSES = (
    ('TODO', 'Todo'),
    ('IN_PROGRESS', 'Inprogress'),
    ('DONE', 'Done'),
)

class Project(models.Model):
    desc = models.CharField(max_length=200)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    summary = models.CharField(max_length=10)
    progress = models.IntegerField(default=0)


class Task(models.Model):
    desc = models.CharField(max_length=200)
    proejct = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    status = models.CharField(max_length=20, choices=STATUSES)
    summary = models.CharField(max_length=10)
    progress = models.IntegerField(default=0)


class Asignee(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    manager = models.ForeignKey("self", on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
