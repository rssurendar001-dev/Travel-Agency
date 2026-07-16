from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Package(models.Model):

    CATEGORY = (
        
        ('India', 'India'),
        
        ('International', 'International'),
        
        ('Europe', 'Europe'),
        
        ('Honeymoon', 'International Honeymoon')
        
    )

    package_name = models.CharField(max_length=100)
    
    category = models.CharField(max_length=30, choices=CATEGORY)
    
    price = models.IntegerField()
    
    image = models.ImageField(upload_to='travels/')
    
    description = models.TextField()

    def __str__(self):
        
        return self.package_name

class Destination(models.Model):

    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    destination_name = models.CharField(max_length=100)
    
    image = models.ImageField(upload_to='travels/')
    
    description = models.TextField()

    days = models.IntegerField()
    
    price = models.IntegerField()

    rating = models.FloatField(default=5)

    international = models.BooleanField(default=False)

    def __str__(self):
        
        return self.destination_name

class Enquiry(models.Model):

    STATUS = (
        
        ('Pending', 'Pending'),
        
        ('Completed', 'Completed'),
        
        ('Cancelled', 'Cancelled')
        
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    travel_date = models.DateField()

    adults = models.IntegerField()

    children = models.IntegerField(default=0)

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    status = models.CharField(max_length=20,choices=STATUS,default='Pending')

    def __str__(self):
        
        return self.user.username

class TravelGoal(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    completed_trip = models.IntegerField(default=0)

    reward = models.BooleanField(default=False)

    def __str__(self):
        
        return self.user.username

class Blog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    destination = models.CharField(max_length=100)

    image = models.ImageField(upload_to='blogs/')

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return self.title

class Memory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    album_name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='travels/')

    caption = models.TextField(blank=True)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        
        return self.album_name

class BudgetPlanner(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total_budget = models.IntegerField()

    transport = models.IntegerField()

    hotel = models.IntegerField()

    food = models.IntegerField()

    shopping = models.IntegerField()

    remaining_budget = models.IntegerField(default=0)

    def __str__(self):
        
        return self.user.username
    
class TravelCost(models.Model):

    HOTEL_TYPE = (

        ('Standard', 'Standard'),

        ('Deluxe', 'Deluxe'),

        ('Luxury', 'Luxury'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    people = models.IntegerField()

    hotel_type = models.CharField(max_length=20,choices=HOTEL_TYPE)

    days = models.IntegerField()

    estimated_cost = models.IntegerField(default=0)

    def __str__(self):
        
        return self.user.username
    
class TravelBuddy(models.Model):

    INTERESTS = (

        ('Adventure', 'Adventure'),
        
        ('Beach', 'Beach'),
        
        ('Nature', 'Nature'),
        
        ('Hill Station', 'Hill Station'),
        
        ('Wildlife', 'Wildlife'),
        
        ('Pilgrimage', 'Pilgrimage'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    travel_date = models.DateField()

    budget = models.IntegerField()

    interest = models.CharField(max_length=50,choices=INTERESTS)

    about = models.TextField()

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user.username

class CurrencyConverter(models.Model):

    CURRENCY_CHOICES = (

        ('INR', 'Indian Rupee'),

        ('USD', 'US Dollar'),

        ('EUR', 'Euro'),

        ('GBP', 'British Pound'),

        ('AED', 'UAE Dirham'),

        ('JPY', 'Japanese Yen'),

        ('SGD', 'Singapore Dollar'),

        ('CAD', 'Canadian Dollar'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.FloatField()

    from_currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES)

    to_currency = models.CharField(max_length=10,choices=CURRENCY_CHOICES)

    converted_amount = models.FloatField(default=0)

    converted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user.username
    
class EmailOTP(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    otp = models.CharField(max_length=6)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):

        return self.user.username