from django.urls import path
from . import views 
from .views import register_view,logout_view,login_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
      # ✅ ADD THIS
      path('contact/', views.contact, name='contact'),
     path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('flights/', views.flight_list, name='flights'),
    path('book/<int:id>/', views.book_flight, name='book_flight'),
path('train/', views.train, name='train'),
path('bus/', views.bus, name='bus'),

path('events/', views.events, name='events'),
path('sports/', views.sports, name='sports'),
path('activities/', views.activities, name='activities'),
path('hotels/', views.hotels, name='hotels'),
path('payment/', views.payment, name='payment'),
path('success/', views.success, name='success'),
    path('download-ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),
path('common-booking/<str:item_type>/<int:item_id>/', views.common_booking, name='common_booking'),
path('common-payment/', views.common_payment, name='common_payment'),
path('payment-success/', views.payment_success, name='payment_success'),
path('movies/', views.movie_page, name='movies'),
path('user_dashboard_x99/', views.user_dashboard_x99, name='user_dashboard_x99'),
]