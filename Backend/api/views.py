from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, decorators
from .models import PreProcessedFiles
from .serializer import PreProcessedFilesSerializer, TokenObtainPairSerializer, RegisterSerializer, ChallengesSerializer
from .serializer import UserDescriptionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework.exceptions import ValidationError
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# models
from Backend.api.models import Challenges

PAGINATION_COUNT = 3
STATUS = {-2: "declined", -1: "failed", 0: "pending", 1: "ongoing", 2: "completed"}

# class PostListView(ListView):
#     model = Challenges
#     template_name = 'blog/home.html'
#     context_object_name = 'challenges'
#     ordering = ['-date_posted']
#     paginate_by = PAGINATION_COUNT
#
#     def get_context_data(self, **kwargs):
#         # Returns a dictionary representing the template context. data is the context here
#         data = super().get_context_data(**kwargs)
#
#         all_users = []
#
#         # idk what is going on lol
#         # data_counter = Challenges.objects.values('user')\
#         #     .annotate(author_count=Count('author'))\
#         #     .order_by('-author_count')[:6]
#
#         data_counter = Challenges.objects.all()
#
#         for aux in data_counter:
#             all_users.append(User.objects.filter(pk=aux['author']).first())
#
#         print(all_users, file=sys.stderr)
#         return data
#
#     def get_queryset(self):
#         user = self.request.user
#         qs = Follow.objects.filter(user=user)
#         follows = [user]
#         for obj in qs:
#             follows.append(obj.follow_user)
#         return Post.objects.filter(author__in=follows).order_by('-date_posted')



#
# def add_post_view(request):
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             messages.success(request, "Challenge post has been created.")
#             return redirect("/posts")
#     form = PostForm()
#     context = {
#         "form": form
#     }
#     return render(request, template_name, context)
#
#
# def display_posts_view(request):
#     posts = Challenges.objects.get_posts(False)
#     challenge_status = []
#     for post in posts:
#         challenge_status.append(STATUS[post.status])
#
#     # zip whatever you wanna display here
#     master_list = zip(posts, challenge_status)
#     context = {
#         "master": master_list
#     }
#
#     return response(request, template_name, context)


@api_view(['GET', 'POST'])
def challenges_list(request):
    if request.method == 'GET':
        challenges = Challenges.objects.all()
        serializer = ChallengesSerializer(challenges, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChallengesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
