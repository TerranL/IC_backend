import uuid
from django.utils import timezone
from django.db import models
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.template.backends import django


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_pic/', null=True, blank=True,
                               default="")

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    """
    def __str__(self):
        return f"Profile - User: {self.user.username} - E-Mail: {self.user.email}"
    """


class Friend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")

    """
    def __str__(self):
        return f"Friendship: {self.user.username} - {self.friend.username}"
    """


class Challenges(models.Model):
    id = models.AutoField(primary_key=True)
    proposer = models.TextField(max_length=10, default="")
    # for now user is the one being challenged
    user = models.TextField(max_length=10, default="")
    title = models.TextField(max_length=100000, default="")
    description = models.TextField(max_length=100000, default="")
    image = models.ImageField(upload_to='challenges', null=True, blank=True)
    # image_path = models.BooleanField()
    # additional fields
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

    objects = models.Manager()


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textbox = models.TextField(max_length=100000)
    image = models.ImageField(upload_to='status', null=True, blank=True)


class Categories(models.Model):
    pass
