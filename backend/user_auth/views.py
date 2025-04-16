from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserDetailSerializer, RoomSerializer, BookingSerializer
from .models import UserProfile, Room, Booking

# Register user and generate token
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

# Login user and return bearer token
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Get authenticated user details
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

# Room views
class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile
        if user_profile.role != 'provider':
            return Response({"error": "Only providers can create rooms"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(provider=user_profile)

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.userprofile != self.get_object().provider:
            return Response({"error": "You can only update your own rooms"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.userprofile != instance.provider:
            return Response({"error": "You can only delete your own rooms"}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

# Booking views
class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_profile = self.request.user.userprofile
        if user_profile.role != 'seeker':
            return Response({"error": "Only seekers can create bookings"}, status=status.HTTP_403_FORBIDDEN)
        room = serializer.validated_data['room']
        if not room.is_available:
            return Response({"error": "Room is not available"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(seeker=user_profile)
        room.is_available = False
        room.save()

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user.userprofile != self.get_object().seeker:
            return Response({"error": "You can only update your own bookings"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user.userprofile != instance.seeker:
            return Response({"error": "You can only delete your own bookings"}, status=status.HTTP_403_FORBIDDEN)
        instance.room.is_available = True
        instance.room.save()
        instance.delete()