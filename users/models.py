from django.db import models

from core.models import TimeStampModels
from rooms.models import Room 

class User(TimeStampModels):
    email         = models.EmailField(max_length=255, unique=True)
    name          = models.CharField(max_length=255)
    password      = models.CharField(max_length=500)
    birthday_date = models.CharField(max_length=45)
    profile_img   = models.CharField(max_length=500, null=True)
    kakao_id      = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "users"

class Host(TimeStampModels):
    nickname      = models.CharField(max_length=255, null=True)
    name          = models.CharField(max_length=255)
    profile_img   = models.CharField(max_length=500)
    is_super_host = models.BooleanField(default=False)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "hosts"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        db_table = "wishlists"