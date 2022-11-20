import django_filters
from django import forms

from .models import Post, Tag

class PostFilter(django_filters.FilterSet):
    headline = django_filters.CharFilter(field_name='headline', lookup_expr='icontains', label='Заголовок')
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(), 
    widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Post
        fields = ['headline', 'tags']