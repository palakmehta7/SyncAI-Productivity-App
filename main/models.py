from django.db import models


STATUSES = (
    ('TODO', 'Todo'),
    ('IN_PROGRESS', 'Inprogress'),
    ('DONE', 'Done'),
)


class Asignee(models.Model):
    name = models.CharField(max_length=2000)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    manager = models.ForeignKey("self", on_delete=models.DO_NOTHING, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.name}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=2000)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    summary = models.CharField(max_length=2000, blank=True, null=True, default=None)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=2000)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    status = models.CharField(max_length=20, choices=STATUSES)
    asignee = models.ForeignKey(Asignee, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    summary = models.CharField(max_length=10, blank=True, null=True, default=None)
    progress = models.IntegerField(default=0)
    pr_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    weightage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.project.name}-{self.name}"
