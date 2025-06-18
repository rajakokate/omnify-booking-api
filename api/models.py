from django.db import models
from django.utils import timezone
# Create your models here.

class FitnessClass(models.Model):
    CLASS_CHOICES = [
        ("Yoga", 'Yoga'),
        ("Zumba", "Zumba"),
        ("HIIT  ", "HIIT")
    ]

    
    name = models.CharField(max_length=20, choices=CLASS_CHOICES)
    datetime = models.DateTimeField 
    instructor = models.CharField(max_length=50)
    available_slots = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.name}on {self.datetime.strftime('%Y-%m-%d %H:%M')}"
    
class Booking(models.Model)
    
    fitness_class = models.ForeignKey(FitnessClass, on_delete= models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_name = models.EmailField()

    def __str__(self):
        return f"{self.client_name} booked {self.fitness_class.name}"
    
    