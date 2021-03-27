from django.contrib import admin
from .models import User, Challenges, Status
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Challenges)
admin.site.register(Status)