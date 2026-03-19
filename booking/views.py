from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import *
from .models import Testimonial
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import time
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import random
import razorpay
@login_required(login_url='login')
def home(request):
    categories = Category.objects.all()
    events = Event.objects.all()
    trending = TrendingExperience.objects.all()
    destinations = Destination.objects.all()
    testimonials = Testimonial.objects.all().order_by('-id')

    return render(request, 'home.html', {
        'categories': categories,
        'events': events,
        'trending': trending,
        'destinations': destinations,
        'testimonials':testimonials,

    })
 


@login_required(login_url='login')
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")

        user = request.user if request.user.is_authenticated else None

        Testimonial.objects.create(
            user=user,   # 👈 IMPORTANT
            name=name,   # 👈 REQUIRED
            review=message
        )

    testimonials = Testimonial.objects.all()
    return render(request, 'contact.html', {'testimonials': testimonials})
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        print("LOGIN HIT")

        email_or_username = request.POST.get('email')
        password = request.POST.get('password')

        print("DATA:", email_or_username, password)

        # 🚨 FIX: Handle empty input
        if not email_or_username or not password:
            messages.error(request, "Please enter all fields")
            return redirect('login')

        # 🔥 SAFE CHECK
        if '@' in email_or_username:
            try:
                user_obj = User.objects.get(email=email_or_username)
                username = user_obj.username
            except User.DoesNotExist:
                username = None
        else:
            username = email_or_username

        user = authenticate(request, username=username, password=password)

        if user:
            print("LOGIN SUCCESS")
            login(request, user)
            return redirect('home')
        else:
            print("LOGIN FAILED")
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')
def register_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 🔥 CHECK IF USER EXISTS
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def flight_list(request):
    flights = Flight.objects.all()

    from_city = request.GET.get('from')
    to_city = request.GET.get('to')
    price = request.GET.get('price')
    arrival = request.GET.get('arrival')
    departure = request.GET.get('departure')

    # 🔍 SEARCH
    if from_city:
        flights = flights.filter(from_city__icontains=from_city.strip())

    if to_city:
        flights = flights.filter(to_city__icontains=to_city.strip())

    # 💰 PRICE
    if price:
        flights = flights.filter(price__lte=price)

    # ✈️ ARRIVAL TIME FILTER
    if arrival:
        start, end = map(int, arrival.split('-'))
        flights = [
        f for f in flights
        if start <= int(f.arrival_time.split(':')[0]) < end
        ]

# 🛫 DEPARTURE
    if departure:
        start, end = map(int, departure.split('-'))
        flights = [
        f for f in flights
        if start <= int(f.departure_time.split(':')[0]) < end
        ]
    airline = request.GET.get('airline')

    if airline:
        flights = flights.filter(name__icontains=airline)
    stops = request.GET.get('stops')

    if stops:
        flights = flights.filter(stops=int(stops))
    return render(request, 'flights.html', {'flights': flights})

@login_required(login_url='login')
def book_flight(request, id):
    flight = Flight.objects.get(id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        flight_class = request.POST.get("flight_class")
        total_price = request.POST.get("total_price")

        Booking.objects.create(
            user=request.user,
            flight=flight,
            name=name,
            email=email,
            phone=phone,
            flight_class=flight_class,
            total_price=total_price
        )

        return redirect("success")

    return render(request, "book.html", {"flight": flight})
@login_required(login_url='login')
def flight_search(request):
    flights = Flight.objects.all()   # 🔥 MUST BE THERE

    return render(request, 'flights.html', {
        'flights': flights
    })
@login_required(login_url='login')
def payment(request):
    if request.method == "POST":

        flight_id = request.POST.get("flight_id")
        total_price = request.POST.get('total_price', 0)

        if total_price == "":
            total_price = 0

        total_price = int(total_price)   # ✅ always convert

        flight = Flight.objects.get(id=flight_id)

        booking_ref = "BK-" + str(random.randint(100000, 999999))

        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            total_price=total_price,
            booking_ref=booking_ref
        )

        return render(request, "payment_success.html", {
            "booking": booking,
            "flight": flight
        })

    return redirect('/')



@login_required(login_url='login')
def download_ticket(request, booking_id):

    booking = Booking.objects.get(id=booking_id)
    flight = booking.flight

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.booking_ref}.pdf"'

    p = canvas.Canvas(response)

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Flight Ticket")

    # Booking Info
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Booking Ref: {booking.booking_ref}")
    p.drawString(50, 730, f"Total Paid: ₹{booking.total_price}")

    # Flight Info
    p.drawString(50, 700, f"From: {flight.from_city}")
    p.drawString(50, 680, f"To: {flight.to_city}")
    
    p.drawString(50, 640, f"Time: {flight.departure_time} - {flight.arrival_time}")

    p.drawString(50, 600, "Thank you for booking!")

    p.showPage()
    p.save()

    return response

def success(request):
    return render(request, "success.html")

def train(request):

    trains = Train.objects.all()

    # 🔍 SEARCH
    from_city = request.GET.get('from')
    to_city = request.GET.get('to')

    if from_city:
        trains = trains.filter(from_city__icontains=from_city)

    if to_city:
        trains = trains.filter(to_city__icontains=to_city)

    # 💺 CLASS FILTER
    travel_class = request.GET.get('class')
    if travel_class:
        trains = trains.filter(classes__icontains=travel_class)

    # 🚆 TRAIN TYPE
    train_type = request.GET.get('train_type')
    if train_type:
        trains = trains.filter(train_type__iexact=train_type)

    # ⏱ DURATION
    duration = request.GET.get('duration')
    if duration:
        if duration == "0-6":
            trains = trains.filter(duration__icontains="6h")
        elif duration == "6-10":
            trains = trains.filter(duration__icontains="8h")
        elif duration == "10-15":
            trains = trains.filter(duration__icontains="10h")
        elif duration == "15+":
            trains = trains.filter(duration__icontains="15h")

    # 📅 DAYS
    days = request.GET.getlist('day')
    if days:
        for d in days:
            trains = trains.filter(days__icontains=d)

    # 💰 PRICE
    price = request.GET.get('price')
    if price:
        trains = trains.filter(price__lte=price)

    return render(request, 'train.html', {'trains': trains})
@login_required(login_url='login')
def common_booking(request, item_type, item_id):

    if item_type == "train":
        item = Train.objects.get(id=item_id)
    if item_type == "bus":
        item = Bus.objects.get(id=item_id)
    tax = 100
    total_price = item.price + tax   # ✅ CALCULATE HERE

    return render(request, "common_booking.html", {
        "item": item,
        "item_type": item_type,
        "total_price": total_price   # ✅ SEND THIS
    })
@login_required(login_url='login')

def common_payment(request):

    if request.method == "POST":

        item_id = request.POST.get("item_id")
        item_type = request.POST.get("item_type")
        total_price = request.POST.get("total_price")

        # 🔥 GET ITEM
        if item_type == "train":
            item = Train.objects.get(id=item_id)
        elif item_type == "bus":
            item = Bus.objects.get(id=item_id)

        # 🔥 CREATE BOOKING (IMPORTANT)
        booking = Booking.objects.create(
            user=request.user,   # ✅ MUST
            flight=None,         # since not flight
            name=request.user.username,
            email=request.user.email,
            booking_ref="BK-" + str(random.randint(100000, 999999)),
            phone="",
            flight_class=item_type,   # use this as type
            total_price=total_price
        )

        return render(request, "common_success.html", {
            "item": item,
            "item_type": item_type,
            "booking": booking
        })

def payment_success(request):

    payment_id = request.GET.get('payment_id')

    return render(request, "common_success.html", {
        "payment_id": payment_id
    })
def bus(request):

    buses = Bus.objects.all()

    # 🔍 SEARCH
    from_city = request.GET.get('from')
    to_city = request.GET.get('to')

    if from_city:
        buses = buses.filter(from_city__icontains=from_city)

    if to_city:
        buses = buses.filter(to_city__icontains=to_city)

    # 🚌 BUS TYPE (AC / NON AC / SLEEPER)
    bus_type = request.GET.get('bus_type')
    if bus_type:
        buses = buses.filter(bus_type__iexact=bus_type)

    # ⏱ DURATION (FIXED - numeric)
    duration = request.GET.get('duration')
    if duration:
        if duration == "0-6":
            buses = buses.filter(duration_hours__lte=6)
        elif duration == "6-10":
            buses = buses.filter(duration_hours__gt=6, duration_hours__lte=10)
        elif duration == "10-15":
            buses = buses.filter(duration_hours__gt=10, duration_hours__lte=15)
        elif duration == "15+":
            buses = buses.filter(duration_hours__gt=15)

    # 📅 BOARDING TIME (NEW FILTER)
    departure_time = request.GET.get('departure_time')
    if departure_time:
        if departure_time == "morning":
            buses = buses.filter(departure_hour__gte=5, departure_hour__lt=12)
        elif departure_time == "afternoon":
            buses = buses.filter(departure_hour__gte=12, departure_hour__lt=17)
        elif departure_time == "evening":
            buses = buses.filter(departure_hour__gte=17, departure_hour__lt=21)
        elif departure_time == "night":
            buses = buses.filter(departure_hour__gte=21)

    # 📍 BOARDING POINT
    boarding = request.GET.get('boarding')
    if boarding:
        buses = buses.filter(from_city__icontains=boarding)

    # 📍 DROP POINT
    drop = request.GET.get('drop')
    if drop:
        buses = buses.filter(to_city__icontains=drop)

    # 💰 PRICE
    price = request.GET.get('price')
    if price:
        buses = buses.filter(price__lte=price)

    return render(request, 'bus.html', {'buses': buses})
def movie_page(request):
    now_showing = Movie.objects.filter(category='now_showing')
    upcoming = Movie.objects.filter(category='upcoming')
    recommended = Movie.objects.filter(category='recommended')

    return render(request, "movies.html", {
        "now_showing": now_showing,
        "upcoming": upcoming,
        "recommended": recommended
    })

@login_required(login_url='login')
@login_required(login_url='login')
def user_dashboard_x99(request):

    bookings = Booking.objects.filter(user=request.user)

    print("LOGGED USER:", request.user)
    print("FILTERED BOOKINGS:", bookings)

    total_x99 = bookings.count()
    confirmed_x99 = bookings.count()
    pending_x99 = 0

    return render(request, 'user_dashboard_x99.html', {
        'bookings_x99': bookings,
        'total_x99': total_x99,
        'confirmed_x99': confirmed_x99,
        'pending_x99': pending_x99,
    })
def events(request):
    return render(request, 'events.html')

def sports(request):
    return render(request, 'sports.html')

def activities(request):
    return render(request, 'activities.html')

def hotels(request):
    return render(request, 'hotels.html')