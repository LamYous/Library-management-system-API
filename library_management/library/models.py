from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'categorie' 

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)  
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            self.available = False
        else:
            self.available = True
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.username} checked out {self.book.title}'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()