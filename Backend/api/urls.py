from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter

from django.urls import path

router = DefaultRouter()
router.register(r'profile-list', views.ProfileViewSet )
router.register(r'friend-list', views.FriendViewSet)

urlpatterns = [
    # Return user Data
    path('user/', views.GetUserAPI.as_view() ,name='get_user'),
    
    # Login page
    path('login/',views.LoginAPI.as_view() ,name='log-in'),

    # Register
    path('register/',views.RegisterAPI.as_view() ,name='register'),
    
    # Register Profile Details (images, date of birth ...)
    path('profile/',views.ProfileAPI.as_view() ,name='profile'),

    path('post_challenges/', views.challenges_list)
]
urlpatterns += router.urls