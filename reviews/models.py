from django.db import models

from core.models import TimeStampModels
from users.models import User
from rooms.models import Room

class Review(TimeStampModels):
    content   = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)
    ratings   = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    room      = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "reviews"