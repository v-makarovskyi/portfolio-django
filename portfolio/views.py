from django.shortcuts import render, redirect
from .models import Post, PostComment
from .forms import CustomUserCreationForm, PostForm, UserForm, ProfileForm
from .filters import PostFilter
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

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
    paginator = Paginator(posts, 3)

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
        return redirect('portfolio:post_detail', slug=post.slug)
    
    context = {'post': post}
    return render(request, 'portfolio/post.html', context)



@admin_only
@login_required(login_url='home')
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('portfolio:posts')
    
    context = {'form': form}
    return render(request, 'portfolio/post_form.html', context)

@admin_only
@login_required(login_url='home')
def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('portfolio:posts')

    context = {'form': form}
    return render(request, 'portfolio/post_form.html', context)


@admin_only
@login_required(login_url='home')
def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    
    context = {'item': post}
    return render(request, 'portfolio/delete.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('portfolio:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'Пользователь с таким email не найден')
        
        if user is not None:
            login(request, user)
            return redirect('portfolio:home')
    
    context = {}
    return render(request, 'portfolio/login.html', context)


def registerPage(request):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			messages.success(request, 'Account successfuly created!')

			user = authenticate(request, username=user.username, password=request.POST['password1'])

			if user is not None:
				login(request, user)

			next_url = request.GET.get('next')
			if next_url == '' or next_url == None:
				next_url = 'portfolio:home'
			return redirect(next_url)
		else:
			messages.error(request, 'An error has occured with registration')
	context = {'form':form}
	return render(request, 'portfolio/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('portfolio:home')

@login_required(login_url='portfolio:home')
def userAccount(request):
    profile = request.user.profile
    comments = PostComment.objects.filter(author=request.user.profile)
    context = {'profile': profile, 'comments':comments}
    
    return render(request, 'portfolio/account.html', context)

@login_required(login_url='portfolio_home')
def updateProfile(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
        
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('portfolio:account')
    
    context = {'form': form}
    return render(request, 'portfolio/profile_form.html', context)









