from django.db import models
from accounts.models import User

class Place(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    imageUrl = models.URLField()

    class Meta:
        abstract = True

class SecondhandSmokingPlace(Place):
    SecondhandSmokingPlaceId = models.AutoField(primary_key=True)
    likes = models.PositiveIntegerField(default=0)

class NoSmokingPlace(Place):
    NoSmokingPlaceId = models.AutoField(primary_key=True)

class SmokingPlace(Place):
    CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    
    SmokingPlaceId = models.AutoField(primary_key=True)
    rate = models.CharField(max_length=1, choices=CHOICES)
    ashtray = models.BooleanField()
    isIndoor = models.BooleanField()

class Likes(models.Model):
    LikesId = models.AutoField(primary_key=True)
    NoSmokingPlaceId = models.ForeignKey(NoSmokingPlace, verbose_name="NoSmokingPlace", on_delete=models.CASCADE)
    userId = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
