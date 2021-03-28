import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile_pic/', null=True, blank=True,
                               default="default/default_avatar.png")
    date_of_birth = models.DateField() 
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Profile - User: {self.user.username} - E-Mail: {self.user.email}"


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_creator")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    created_at = models.DateField(auto_now_add=True)
    """
    def __str__(self):
        return f"Friendship: {self.user.username} - {self.friend.username}"
    """

class Challenges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textbox = models.TextField(max_length=100000, default="")
    image = models.ImageField(upload_to='challenges', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post: {self.user.username} - {self.created_at}"

class Status(models.Model):
    challenge = models.OneToOneField(Challenges, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textbox = models.TextField(max_length=100000, default="")
    image = models.ImageField(upload_to='status', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status: {self.user.username} - {self.created_at}"

class Categories(models.Model):
    pass
