from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey("Category", related_name='events', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='events')
    image = models.ImageField(upload_to='event_images/',  default='event_images/default.jpg')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
