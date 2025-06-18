from rest_framework import serializers
from .models import FitnessClass, Booking

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FitnessClass
        fields = "__all__" #it includes all fields: name,datetime, instructor, available_shots

class BookingSerializer (serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"  #it includes fitness_class, client_name, client_email