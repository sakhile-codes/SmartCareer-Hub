
from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    # Add more fields as needed

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    posted_date = models.DateField()
    deadline = models.DateField()
    skills_required = models.TextField()
    experience_required = models.CharField(max_length=100)
    # Add more fields as needed

class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    learning_time = models.CharField(max_length=50)
    learning_link = models.URLField()
    # Add more fields as needed

class LearnEarnOpportunity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    # Add more fields as needed