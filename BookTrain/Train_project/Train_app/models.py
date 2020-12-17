from django.db import models

# Create your models here.
class TicketModel(models.Model):
    Ticket_id = models.IntegerField(null=True)
    Train_number = models.IntegerField()
    Train_name = models.CharField(max_length=256)
    Origin = models.CharField(max_length=100)
    Destination = models.CharField(max_length=100)
    Departure = models.CharField(max_length=100)
    Arrival = models.CharField(max_length=100)
    Travel_time = models.CharField(max_length=100)
    Date = models.CharField(max_length=100)
    Day = models.CharField(max_length=100)
    Class = models.CharField(max_length=100)
    Price = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    Payment = models.CharField(max_length=100, null=True)


    def __str__(self):
        return str(self.Ticket_id)


class PassengerModel(models.Model):
    ticket = models.ForeignKey('Train_app.TicketModel', null=True, related_name="passengers", on_delete=models.CASCADE)
    Passenger_name = models.CharField(max_length=256)
    Age = models.PositiveIntegerField()
    Gender = models.CharField(max_length=200)
    Berth = models.CharField(max_length=256)


    def __str__(self):
        return self.Passenger_name
