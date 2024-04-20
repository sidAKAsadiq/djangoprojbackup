from django.contrib import admin

# Register your models here.

#to view our models in admin pannel
from .models import *
admin.site.register(Room)   
admin.site.register(Topic)   
admin.site.register(Message)   