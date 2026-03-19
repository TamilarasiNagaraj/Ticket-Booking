from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='events/')
    description = models.TextField()

    def __str__(self):
        return self.title
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')
    icon = models.CharField(max_length=10, blank=True)  # emoji/icon

    def __str__(self):
        return self.name
    
class TrendingExperience(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)  # Music, Flight, Activity
    location = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='trending/')
    rating = models.IntegerField(default=5)
    def __str__(self):
        return self.title
class Destination(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
   
    price = models.IntegerField()
    rating = models.FloatField(default=4.3)
    image = models.ImageField(upload_to='destinations/')
    is_hot = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    review = models.TextField()

    def __str__(self):
        return self.name
    
class Flight(models.Model):
    name = models.CharField(max_length=100)  # IndiGo

    from_city = models.CharField(max_length=100)
    from_code = models.CharField(max_length=10)  # MAA

    to_city = models.CharField(max_length=100)
    to_code = models.CharField(max_length=10)  # DEL

    departure_time = models.CharField(max_length=20)  # 08:00 AM
    arrival_time = models.CharField(max_length=20)    # 12:05 PM

    duration = models.CharField(max_length=20)  # 2h 45m

    price = models.IntegerField()

    stops = models.IntegerField(default=0)  # 0 = Non stop

    logo = models.ImageField(upload_to='airlines/', null=True, blank=True)

    def __str__(self):
        return self.name
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    booking_ref = models.CharField(max_length=20)   
    phone = models.CharField(max_length=15)
    flight_class = models.CharField(max_length=10)
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Train(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)

    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)

    departure_time = models.CharField(max_length=10)
    arrival_time = models.CharField(max_length=10)

    duration = models.CharField(max_length=20)

    train_type = models.CharField(max_length=50)  # superfast, express
    classes = models.CharField(max_length=100)    # SL, 3A, etc
    days = models.CharField(max_length=100)       # Mon, Tue...

    price = models.IntegerField()

    def __str__(self):
        return self.name
class Bus(models.Model):
    name = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=50)  # AC / Non AC
    price = models.IntegerField()

    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)

    departure_time = models.CharField(max_length=20)
    arrival_time = models.CharField(max_length=20)

    amenities = models.TextField()
    duration = models.CharField(max_length=20)

    def __str__(self):
        return self.name
class Movie(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    image = models.ImageField(upload_to='movies/')
    duration = models.CharField(max_length=20, blank=True)
    showtimes = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=20)  # now_showing / upcoming / recommended

    def __str__(self):
        return self.name