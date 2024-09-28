

# Create your models here.
from django.db import models

class CVUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
