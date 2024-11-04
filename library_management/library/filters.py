from .models import Book

import django_filters

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    
    class Meta:
        model = Book
        fields = ['title', 'category']