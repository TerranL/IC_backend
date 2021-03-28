from django.conf.urls import url, include
from . import views

from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from django.urls import path

urlpatterns = [
    path('post_challenges/', views.challenges_list)
]

urlpatterns = format_suffix_patterns(urlpatterns)