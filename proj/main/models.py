from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Topic(models.Model):
    name = models.TextField(max_length = 100)
    
    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User , on_delete = models.CASCADE, null = True) 
    topic = models.ForeignKey(Topic , on_delete = models.SET_NULL , null = True)
    name = models.CharField(max_length = 50,null = True , blank = True)
    description = models.TextField(max_length = 150,null = True , blank = True)
    members = models.ManyToManyField(User , related_name= "members" , blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User , on_delete = models.CASCADE) 
    room = models.ForeignKey(Room , on_delete = models.CASCADE)
    matter = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class meta:
        ordering = ['-updated' , '-created']

    def __str__(self) -> str:
        return self.matter[0 : 50] #only 10 characeters   
    
class User(AbstractUser):
    