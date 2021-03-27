from django.conf.urls import url, include
from . import views
from knox.urls import views as knoxviews

from django.urls import path

urlpatterns = [
    #
    path('user/', views.GetUserAPI.as_view() ,name='get_user'),
    
    # Login page
    path('login/',views.LoginAPI.as_view() ,name='log-in'),

    # Register
    path('register/',views.RegisterAPI.as_view() ,name='register'),

    #
    #path('log-out/',knoxviews.LogoutView.as_view() ,name='log-out'),
    
    path('profile/',views.ProfileAPI.as_view() ,name='profile'),


]