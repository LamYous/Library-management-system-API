from django.shortcuts import render, get_object_or_404
from .models import Book, Category, Checkout
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import BookSerializer, CategorySerializer, CheckoutSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.models import User

from django.utils import timezone
# from .filters import BookFilter
# from django.db.models import Q

#------------------views--------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_list(request):
    all_books = Book.objects.all()
    total_books = all_books.count()
    
    serializer = BookSerializer(all_books, many=True)
    return Response({"total_books":total_books, "All books":serializer.data,}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_books(request):
    available_books = Book.objects.filter(available=True)
    
    serializer = BookSerializer(available_books, many=True)
    return Response({"Available books":serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_book(request):
    title = request.query_params.get('title', None)
    category = request.query_params.get('category', None)

    queryset = Book.objects.all()

    if title:
        queryset = queryset.filter(title__icontains=title)
    
    if category:
        queryset = queryset.filter(category__name__icontains=category)
        
    # search by title: books/search/?title=....
    # search by category: books/search/?category=....
    # combine: books/search/?title=....&category=....

    serializer = BookSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def edit_book(request, book_id):
    book = get_object_or_404(id=book_id)

    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_book(request, book_id):
    book = get_object_or_404(id=book_id)
    book.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    categorys = Category.objects.all()
    serializer = CategorySerializer(categorys, many=True)
    return Response({"categorys":serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_category(request):
    data = request.data
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    serializer = CategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(request, book_id):
    category = get_object_or_404(id=book_id)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def checkout_book(request):
    user_id = request.data.get('user')
    book_id = request.data.get('book')

    if not user_id or not book_id:
        return Response({'error': 'User ID and Book ID are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(pk=user_id) 
        book = Book.objects.get(pk=book_id)

        if not book.available or book.quantity <= 0:
            return Response({'error': 'Book is not available for checkout.'}, status=status.HTTP_400_BAD_REQUEST)

        checkout = Checkout.objects.create(
            user=user,
            book=book,
            due_date= timezone.now() + timezone.timedelta(days=14)
            )
        book.quantity -= 1
        book.save()

        return Response({'message': 'Book checked out successfully.', 'checkout_id': checkout.id}, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Book.DoesNotExist:
        return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        # Catch any other exceptions and return a 500 error
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def return_book(request, checkout_id):
    try:
        # Retrieve the checkout record
        checkout = Checkout.objects.get(id=checkout_id)
        book = checkout.book

        # Delete the checkout record to mark the book as returned
        checkout.delete()

        # Update the book's quantity
        book.quantity += 1
        book.save()

        return Response({'message': 'Book returned successfully.'}, status=status.HTTP_200_OK)

    except Checkout.DoesNotExist:
        return Response({'error': 'Checkout record not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def checkout_list(request):
    checkouts = Checkout.objects.all()
    serializer = CheckoutSerializer(checkouts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def user_list(request):
    try:
        users = User.objects.all()
        user_data = []
        count = users.count()

        for user in users:
            profile = getattr(user, 'userprofile', None)  # Access the related UserProfile
            checkouts = Checkout.objects.filter(user=user).values('id', 'book__title', 'checkout_date', 'due_date')

            user_data.append({
            'id':user.id,
            'username': user.username,
            'email': user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email': user.email,
            'phone_number': profile.phone_number if profile else None,
            'address':profile.address if profile else None,
            'checkouts': list(checkouts)
        })
            
        return Response({"count":count,"users":user_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user = request.user  # Get the currently authenticated user
        profile = user.userprofile  # Access the related UserProfile

        if request.method == 'GET':
            
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'phone_number': profile.phone_number if profile else None,
                'address': profile.address if profile else None,
            }
            return Response(user_data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            
            data = request.data
            
            # Update user fields
            user.email = data.get('email', user.email)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.save()

            # Update profile fields
            if profile:
                profile.phone_number = data.get('phone_number', profile.phone_number)
                profile.address = data.get('address', profile.address)
                profile.save()

            return Response({'message': 'Profile updated successfully.'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
