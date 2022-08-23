from tkinter import CASCADE
from django.db import models
from kanban_board.models import KanbanBoard

# Create your models here.
class KanbanUser(models.Model):
    group_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_created=True)
    # for kanban group and board relationship (M2M)
    board = models.ManyToManyField(KanbanBoard, blank=True, related_name="board")

    class Meta:
        ordering = ["date_created", "group_name"]
