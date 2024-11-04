from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='books'),
    path('books/new/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name="edit_book"),
    path('books/delete/<int:book_id>/', views.delete_book, name="delete_book"),

    path('books/available/', views.available_books, name="available_books"),
    path('books/search/', views.search_book, name="search_book"),

    path('categories/', views.category_list, name='categories'),
    path('categories/new', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name="edit_category"),
    path('categories/delete/<int:category_id>/', views.delete_category, name="delete_category"),

    path('checkout/', views.checkout_book, name='checkout_book'),
    path('return/<int:checkout_id>/', views.return_book, name='return_book'),

    path('checkouts/', views.checkout_list, name='checkout_list'),

    path('users/', views.user_list, name='user_list'),
    path('profile/', views.user_profile, name='user_profile')

]
