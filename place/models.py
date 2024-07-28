from django.db import models

class Place(models.Model):
    placeId = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=255)
    imageUrl = models.URLField()

class SecondhandSmokingPlace():
    SecondhandSmokingPlaceId = models.AutoField(primary_key=True)
    placeId = models.ForeignKey(Place, verbose_name = "Place", on_delete=models.CASCADE)

class NoSmokingPlace():
    NoSmokingPlaceId = models.AutoField(primary_key=True)
    placeId = models.ForeignKey(Place, verbose_name = "Place", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class SmokingPlace():
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