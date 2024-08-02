# Generated by Django 5.0.7 on 2024-08-02 15:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NoSmokingPlace',
            fields=[
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('placeId', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReportSmokingPlace',
            fields=[
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('placeId', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], max_length=1)),
                ('ashtray', models.BooleanField(default=True)),
                ('isIndoor', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SecondhandSmokingPlace',
            fields=[
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('placeId', models.AutoField(primary_key=True, serialize=False)),
                ('likesCount', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SmokingPlace',
            fields=[
                ('latitude', models.FloatField(default=0.0)),
                ('longitude', models.FloatField(default=0.0)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('placeId', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('LikesId', models.AutoField(primary_key=True, serialize=False)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('SecondHandSmokingPlaceId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='place.secondhandsmokingplace', verbose_name='NoSmokingPlace')),
            ],
        ),
    ]
