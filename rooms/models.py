from django.db import models
from django.core.validators import MinValueValidator

class Region(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "regions"

class Room(models.Model):
    name          = models.CharField(max_length=255)
    description   = models.TextField
    thumbnail_img = models.CharField(max_length=500)
    price         = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    max_guest     = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_pet       = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    check_in      = models.DateField()
    check_out     = models.DateField()
    bedroom       = models.CharField(max_length=10)
    bed_count     = models.CharField(max_length=10)
    latitude      = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)
    longitude     = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)
    address       = models.CharField(max_length=500)
    region        = models.ForeignKey(Region, on_delete=models.CASCADE)
    host          = models.ForeignKey("users.Host", on_delete=models.CASCADE)
    facilities    = models.ManyToManyField("Facility", db_table="room_facilities")
    types         = models.ManyToManyField("Type", db_table="room_types")
    categories    = models.ManyToManyField("Category", db_table="room_categories")
    
    class Meta:
        db_table = "rooms"

class RoomImage(models.Model):
    image_url = models.CharField(max_length=1000)
    room      = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room")

    class Meta:
        db_table = "room_images"

class Facility(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "facilities"

class Type(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "types"

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "categories"