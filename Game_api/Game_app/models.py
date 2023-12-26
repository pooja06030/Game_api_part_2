from django.db import models
from django.db import models
from django.db import models
from django.db import models


# Create your models here.


class Developer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    address = models.CharField(max_length=200)
    privacy_policy = models.TextField(max_length=500)
    create_at = models.DateField(auto_now_add=False)
    update_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class device_frant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class GameMaker(models.Model):
    GAME_TYPE_CHOICES = [
        ('HTML', 'HTML '),
        ('Cloud', 'Cloud'),
        ('Native', 'Native'),
    ]
    id = models.AutoField(primary_key=True)
    short_description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    include_ads = models.BooleanField(default=True)
    developer = models.ForeignKey(
        Developer, on_delete=models.CASCADE, default=1)
    device = models.ForeignKey(
        device_frant, on_delete=models.CASCADE, default=1)
    game_name = models.CharField(max_length=100)
    game_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    game_type = models.CharField(
        max_length=10, choices=GAME_TYPE_CHOICES, default='HTML')

    def __str__(self):
        return self.game_name


class custom_user(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=False,null=False)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    

class User(models.Model):
    username=models.CharField(max_length=30)
    email=models.CharField(max_length=200, default=True)
    is_verified=models.BooleanField(default=False)
    otp=models.IntegerField(blank=True)



# Create your models here.
