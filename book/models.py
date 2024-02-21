from django.db import models
import uuid


class Book(models.Model):
    """
    Model representing a book.
    This model stores information about a book including its title, author, published date, and a unique identifier.
    
    """
    Title = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Published_Date = models.DateField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.Title