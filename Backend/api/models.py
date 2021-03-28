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

    # user 1 is the challenge initiator
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    textbox = models.TextField(max_length=100000, default="")
    image = models.ImageField(upload_to='challenges', null=True, blank=True)
    # additional fields
    date_posted = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0) # status: -2:declined, -1:failed, 0:pending, 1:ongoing, 2:completed

    objects = models.Manager()



    # def save(self):
    #     super().save()
    #     if self.image:
    #         img = Image.open(self.image.path)
    #
    #         if img.height > 300 or img.width > 300:
    #             output_size = (600, 600)
    #             img.thumbnail(output_size)
    #             img.save(self.img.path)


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textbox = models.TextField(max_length=100000)
    image = models.ImageField(upload_to='status', null=True, blank=True)


class Categories(models.Model):
    pass
