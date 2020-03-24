from django.db import models

# Create your models here.
class Post(models.Model):
    post = models.CharField(max_length=500)