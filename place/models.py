from django.db import models
from accounts.models import User

class Place(models.Model):
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        abstract = True

class SecondhandSmokingPlace(Place):
    placeId = models.AutoField(primary_key=True)
    likesCount = models.PositiveIntegerField(default=0)

class NoSmokingPlace(Place):
    placeId = models.AutoField(primary_key=True)

class SmokingPlace(Place):
    placeId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)

class ReportSmokingPlace(Place):
    placeId = models.AutoField(primary_key=True)
    CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    rate = models.CharField(max_length=1, choices=CHOICES)
    ashtray = models.BooleanField(default=True)
    isIndoor = models.BooleanField(default=True)


class Likes(models.Model):
    LikesId = models.AutoField(primary_key=True)
    SecondHandSmokingPlaceId = models.ForeignKey(SecondhandSmokingPlace, verbose_name="NoSmokingPlace", on_delete=models.CASCADE)
    userId = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
