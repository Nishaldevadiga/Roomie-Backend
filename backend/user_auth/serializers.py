from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Room, Booking

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role', 'phone_number', 'bio']

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(write_only=True)  # Used for nested profile creation

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def to_representation(self, instance):
        return {
            'username': instance.username,
            'email': instance.email,
            'profile': UserProfileSerializer(instance.userprofile).data
        }

class UserDetailSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

class RoomSerializer(serializers.ModelSerializer):
    provider = UserProfileSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'provider', 'title', 'description', 'price', 'location', 'is_available', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    seeker = UserProfileSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'seeker', 'room', 'start_date', 'end_date', 'total_price', 'status', 'created_at']
