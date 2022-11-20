from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=200)
    avatar = models.ImageField(null=True, blank=True, upload_to='images', default='/user.png')
    bio = models.TextField(null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        name = str(self.first_name)
        if self.last_name:
            name += ' ' + str(self.last_name)
        return name

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    headline = models.CharField('заголовок', max_length=150)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='images', default='/media/placeholder.png')
    body = RichTextUploadingField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.headline
    
    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.headline)
        
            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.headline) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()
        
        super().save(*args, **kwargs)

class PostComment(models.Model):
    author = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE) 
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.body
    
    @property
    def created_dynamic(self):
        now = timezone.now()
        return now

        
