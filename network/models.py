from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related


class User(AbstractUser):
    pass

class User_Following(models.Model):
    # A is following B
    user_A = models.ForeignKey(User, on_delete=models.CASCADE, related_name="random1")
    user_B = models.ForeignKey(User, on_delete=models.CASCADE, related_name="random2")

class Post(models.Model):
    post = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post} is liked by {self.liked_by}"