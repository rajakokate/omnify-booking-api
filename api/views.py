from django.shortcuts import render
from pytz import timezone as pytz_timezone
from django.conf import settings

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

        tz_param = request.query_params.get('tz', 'Asia/Kolkata') # By default tz is India
        try:
            user_tz = pytz_timezone(tz_param)
        except Exception:
            return Response({"error":"Invalid TimeZone"}, status= status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        classes = FitnessClass.objects.filter(datetime__gte= now).order_by("datetime")

        #Converting datetimes to requested timezone
        data =[]
        for cls in classes:
            localized_time = cls.datetime.astimezone(user_tz)
            data.append({
                "id":cls.id,
                "name":cls.name,
                "datetime": localized_time.strftime("%Y-%m-%d %H:%M:%S"),
                "instructor": cls.instructor,
                "available_slots": cls.available_slots
            })
        return Response(data)
    
    
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
    

