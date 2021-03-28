from django.contrib import admin
from .models import User, Friend, Challenges, Status, Categories, Profile
from django.contrib.auth.admin import UserAdmin



admin.site.register(Challenges)
admin.site.register(Status)
admin.site.register(Friend)
admin.site.register(Categories)
admin.site.register(Profile)