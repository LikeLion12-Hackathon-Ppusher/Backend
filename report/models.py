from django.db import models
from place.models import SmokingPlace, SecondhandSmokingPlace
from accounts.models import User

class Report(models.Model):
    CHOICES = (
        ('SH', '간접 흡연 구역'),
        ('SM', '흡연 구역')
    )
    # PK
    reportId = models.AutoField(primary_key=True)

    # FK
    smokingPlace = models.ForeignKey(SmokingPlace, null=True, blank=True, on_delete=models.CASCADE)
    secondhandSmokingPlace = models.ForeignKey(SecondhandSmokingPlace, null=True, blank=True, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    # field
    description = models.TextField(verbose_name="Description", max_length=100)
    reportType = models.CharField(choices=CHOICES, max_length=2)
