from django.db import models

class Report():
    CHOICES = (
        ('SH', '간접 흡연 구역'),
        ('SM', '흡연 구역')
    )
    # PK
    reportId = models.AutoField(primary_key=True)

    # FK
    placeId = models.ForeignKey("place.modelsPlace", related_name="place", on_delete=models.CASCADE)
    userId = models.ForeignKey("accounts.modelsUser", related_name="user", on_delete=models.CASCADE)

    # field
    description = models.TextField(verbose_name = "상세 정보", max_length=100)
    reportType = models.CharField(choices=CHOICES, max_length=2)
