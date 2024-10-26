from django.db import models
from django.db.models import Avg


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

class Board(models.Model):
    name = models.CharField(max_length=2000)
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    last_synced_at = models.DateField("last synced at", blank=True, null=True, default=None)


    def __str__(self):
        return f"{self.name}"

class Project(models.Model):
    board = models.ForeignKey(Board, on_delete=models.DO_NOTHING)
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
    summary = models.TextField(blank=True, null=True, default=None)
    progress = models.IntegerField(default=0)
    pr_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    weightage = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return f"{self.project.name}-{self.name}"
    
    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        avg_progress = self.project.task_set.aggregate(avg=Avg("progress")).get("avg") or 0
        self.project.progress = avg_progress
        self.progress.save()
        return super().save(force_insert, force_update, using, update_fields)
