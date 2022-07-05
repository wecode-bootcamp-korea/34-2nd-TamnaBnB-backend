from django.db import models

from core.models import TimeStampModels
from users.models import User
from rooms.models import Room

class ReservationStatus(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "reservation_tatus"

class Reservation(TimeStampModels):
    reservation_number = models.CharField(max_length=14)
    accomodation_fee   = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    check_in_date      = models.DateField()
    check_out_date     = models.DateField()
    num_of_guest       = models.IntegerField(null=False)
    num_of_pet         = models.IntegerField(default=0, null=True)
    user               = models.ForeignKey(User, on_delete=models.CASCADE) 
    room               = models.ForeignKey(Room, on_delete=models.CASCADE)
    status             = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = "reservations"