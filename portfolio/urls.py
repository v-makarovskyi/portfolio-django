from django.urls import path
from .views import home, posts, post

app_name = 'portfolio'

urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('post/<slug:slug>/', post, name='post_detail'),
]