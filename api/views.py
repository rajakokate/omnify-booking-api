from django.shortcuts import render

# Create your views here.
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

#GET /classes
class FitnessClassList(APIView):
    def get (self, request):
        now = timezone.now()
        classes = FitnessClass.objects.filter(datetime__get= now).order_by("datetime")
        serializer = FitnessClassSerializer(classes, many=True)
        return Response(serializer.data)
#POST /book
class BookClass (APIView):
    def post (self, request):
        serializer=BookingSerializer(data = request.data)
        if serializer.is_valid():
            fitness_Class = serializer.validated_data['fitness_class']
            if fitness_Class.available_slots > 0:
                fitness_Class.available_slots -=1
                fitness_Class.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "No slots available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#GET /bookings?email = 
class BookingList(APIView):
    def get (self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error":"Email Parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        bookings = Booking.objects.filter(client_email = email)
        serializer = BookingSerializer(bookings,many = True)
        return Response(serializer.data)