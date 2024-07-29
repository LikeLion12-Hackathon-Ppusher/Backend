from django.db import models
from accounts.models import *

class Place(models.Model):
    placeId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255)
    imageUrl = models.URLField()

class SecondhandSmokingPlace(models.Model):
    SecondhandSmokingPlaceId = models.AutoField(primary_key=True)
    placeId = models.ForeignKey(Place, verbose_name = "Place", on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)

class NoSmokingPlace(models.Model):
    NoSmokingPlaceId = models.AutoField(primary_key=True)
    placeId = models.ForeignKey(Place, verbose_name = "Place", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class SmokingPlace(models.Model):
    CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    
    SmokingPlaceId = models.AutoField(primary_key=True)
    placeId = models.ForeignKey(Place, verbose_name = "Place", on_delete=models.CASCADE)
    rate = models.CharField(max_length=1, choices=CHOICES)
    ashtray = models.BooleanField()
    
class Likes(models.Model):
    LikesId = models.AutoField(primary_key=True)
    NoSmokingPlaceId = models.ForeignKey(NoSmokingPlace, verbose_name = "NoSmokingField", on_delete=models.CASCADE)
    userId = models.ForeignKey(User, verbose_name= "User", on_delete= models.CASCADE)