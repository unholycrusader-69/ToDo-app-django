from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ToDo(models.Model):
    title = models.CharField(max_length=100)
    finished = models.BooleanField(default= False)
    deadline = models.DateField(null=True ,blank= True)
    deadline_time = models.TimeField(null = True,blank= True)

    def __str__(self):
        return self.title
   
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username}"
    
class UserNote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    page_one = models.TextField(blank=True)
    page_two = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Notes"