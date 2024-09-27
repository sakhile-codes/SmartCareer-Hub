from django.contrib import admin

# Register your models here.
from .models import Profile, Job, Skill, LearnEarnOpportunity

admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Skill)
admin.site.register(LearnEarnOpportunity)