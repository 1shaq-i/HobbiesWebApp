from django.db import models
from django.contrib.auth.models import AbstractUser


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"


class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)
    friends_list = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username


class FriendRequests(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_friend_requests'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_friend_requests'
    )

    def __str__(self):
        return f"{self.sender} sent a friend request to {self.receiver}"
