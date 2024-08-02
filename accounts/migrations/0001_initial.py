# Generated by Django 5.0.7 on 2024-08-02 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userId', models.CharField(max_length=20, unique=True)),
                ('userType', models.CharField(choices=[('SY', '흡연자'), ('SN', '비흡연자')], max_length=2)),
                ('kakaoEmail', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('M', '남자'), ('F', '여자')], max_length=1)),
                ('distance', models.IntegerField(choices=[(0, '10M'), (1, '20M'), (2, '30M')], default=0, null=True)),
                ('time', models.IntegerField(choices=[(0, '즉시'), (1, '5분'), (2, '10분')], default=0, null=True)),
                ('option', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'accounts_user',
            },
        ),
    ]
