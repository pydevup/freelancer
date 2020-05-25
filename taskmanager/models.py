from django.db import models
from django.contrib.auth.models import User

import os

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, default=None)
    bio = models.TextField(max_length=500, default=None)
    gender = models.CharField(max_length=10, choices=(("Male", "Male"), ("Female", "Female")), default="Male", blank=False)
    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        os.remove(self.image.name)
        super(CustomUser, self).delete(*args, **kwargs)

class Project(models.Model):
    project_name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=300, default=None)
    postedOn = models.DateTimeField(auto_now_add=True, blank=True)
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #applicants = models.ManyToManyField(CustomUser)
    isCompleted = models.BooleanField(default=False)
    deadline = models.DateField(blank=False)
    def __str__(self):
        return self.project_name



