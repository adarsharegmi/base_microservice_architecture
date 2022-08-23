from django.db import models

# Create your models here.
class KanbanBoard(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField()
    description = models.CharField(max_length=1000)
    nickname = models.CharField(max_length=50)
