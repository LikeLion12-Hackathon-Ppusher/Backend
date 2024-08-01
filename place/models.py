from django.db import models
from accounts.models import User

class Place(models.Model):
    placeId = models.AutoField(primary_key=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    imageUrl = models.URLField(default="")

class SecondhandSmokingPlace(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True, db_column='placeId')
    likes = models.PositiveIntegerField(default=0)

class NoSmokingPlace(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True, db_column='placeId')

class SmokingPlace(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True, db_column='placeId')
    CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    rate = models.CharField(max_length=1, choices=CHOICES)
    ashtray = models.BooleanField()
    isIndoor = models.BooleanField()

class Likes(models.Model):
    LikesId = models.AutoField(primary_key=True)
    NoSmokingPlaceId = models.ForeignKey(NoSmokingPlace, verbose_name="NoSmokingPlace", on_delete=models.CASCADE)
    userId = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
