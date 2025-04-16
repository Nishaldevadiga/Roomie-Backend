from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, RoomListCreateView, RoomDetailView, BookingListCreateView, BookingDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('rooms/', RoomListCreateView.as_view(), name='room_list_create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
]