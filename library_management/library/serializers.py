from rest_framework import serializers
from .models import Book, Category, Checkout

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class CheckoutSerializer(serializers.ModelSerializer):
    checkout_date = serializers.DateField(format="%Y-%m-%d")  # Format as needed
    due_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Checkout
        fields = '__all__'