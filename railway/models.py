from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Station(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    city = models.CharField(max_length=100, default="Unknown")   
   
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
class SeatCategory(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    seat_fare = models.DecimalField(max_digits=10, decimal_places=2)

class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)
    number = models.CharField(max_length=10, unique=True)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="source_station")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination_station")
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.IntegerField()
    base_fare = models.FloatField()

    def clean(self):
        if self.source == self.destination:
            raise ValidationError("Source and destination cannot be the same")
        #add Validation for arrival time > departure time, base fare > 0, duration > 0
       
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name} ({self.number})"

class HaltStation(models.Model):
    
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    arrival_time = models.TimeField(null=True)
    departure_time = models.TimeField(null=True)
    # halt_duration = models.DurationField()
    order = models.IntegerField(null=True)

    class Meta:
        unique_together = ('station', 'route', 'order')

    def __str__(self):
        return f"Halt-{self.station} on route-({self.route})"
    
class Train(models.Model):
    pass