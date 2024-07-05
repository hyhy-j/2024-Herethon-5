from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from accounts.models import CustomUser

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='popplace_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='popplace_user_set', blank=True)

class Column(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='events')

class Location(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class PopupStore(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='popup_images/', null=True, blank=True)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    # homepage = models.URLField(max_length=200, blank=True, null=True)
    # sns = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    YES_NO_CHOICES = (
        ('yes', '예'),
        ('no', '아니오'),
    )
    popup_store = models.ForeignKey(PopupStore, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)
    video = models.FileField(upload_to='review_videos/', null=True, blank=True)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    sustainability_rating = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='yes')
    positive_rating = models.CharField(max_length=3, choices=YES_NO_CHOICES, default='yes')
    rate = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))])

    def __str__(self):
        return self.title

class Stamp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='popplace_stamps')
    code = models.CharField(max_length=20)
    date_received = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    popup_store = models.ForeignKey(PopupStore, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.popup_store.name}'

class Reservation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='popplace_reservations')
    popup_store = models.ForeignKey(PopupStore, on_delete=models.CASCADE, related_name='popplace_reservations')
    date = models.DateField()
    time = models.TimeField()
    participant = models.PositiveIntegerField()
