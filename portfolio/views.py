from django.shortcuts import render, redirect
from .models import Post, PostComment
from .forms import CustomUserCreationForm, PostForm, UserForm, ProfileForm
from .filters import PostFilter
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate

#home
def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]
    context = {'posts':posts}

    return render(request, 'portfolio/home.html', context)

#posts_list
def posts(request):
    posts = Post.objects.filter(active=True)
    my_filter = PostFilter(request.GET, queryset=posts)
    posts = my_filter.qs

    page = request.GET.get('page')
    paginator = Paginator(posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {'posts':posts, 'my_filter': my_filter}
    return render(request, 'portfolio/posts.html', context)



#post_single
def post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        PostComment.objects.create(
            author = request.user.profile,
            post = post, 
            body = request.POST['comment']
        )
        messages.success(request, 'Ваш комментарий успешно опубликован')
        return redirect('post', slug=post.slug)
    
    context = {'post': post}
    return render(request, 'portfolio/post.html', context)


def register(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Аккаунт успешно создан')

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
            
            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Ошибка регистрации. Попробуйте позже')
        
        context = {'form': form}
        return render(request, 'portfolio/register.html', context)





