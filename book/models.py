from django.db import models
import uuid

# Create your models here.

class Book(models.Model):
    Title = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Published_Date = models.DateField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.Title