from django.conf.urls import url, include
from . import views
from knox.urls import views as knoxviews

from django.urls import path

urlpatterns = [
    # Return user Data
    path('user/', views.GetUserAPI.as_view() ,name='get_user'),
    
    # Login page
    path('login/',views.LoginAPI.as_view() ,name='log-in'),

    # Register
    path('register/',views.RegisterAPI.as_view() ,name='register'),
    
    # Register Profile Details (images, date of birth ...)
    path('profile/',views.ProfileAPI.as_view() ,name='profile'),
]