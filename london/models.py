from django.db import models

class Buses(models.Model):
    line_name = models.CharField(max_length=5)
    destination_name = models.CharField(max_length=15)
    vehicle_id = models.CharField(max_length=10, unique=True)
    expected_arrival = models.DateTimeField('expected')
    time_now = models.DateTimeField('time Now')

    def __str__(self):
        return self.vehicle_id
