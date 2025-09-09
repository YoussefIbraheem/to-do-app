from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class ToDo(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending" , "Pending"
        IN_PROGRESS = "in_progress" , "In Progress"
        COMPLETED = "completed" , "Completed"
        CANCELLED = "cancelled" , "Cancelled"
    
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    status = models.CharField(choices=StatusChoices,default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.title
    