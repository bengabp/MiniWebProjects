from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    unique_id = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    author  = models.ForeignKey(User,on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,models.CASCADE)
