from django.urls import path
from .views import *

app_name = 'portfolio'

urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('post/<slug:slug>/', post, name='post_detail'),
   
    path('create_post/', create_post, name='create_post'),
    path('post/update_post/<slug:slug>/', update_post, name='update_post'),
    path('post/delete/<slug:slug>/', delete_post, name='delete_post'),
    
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name='logout'),

    path('account/', userAccount, name='account'),
    path('update_profile/', updateProfile, name='update_profile'),
]