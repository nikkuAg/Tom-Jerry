from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator

# Create your models here.

PHONE_NUMBER_REGEX = RegexValidator(
    r'^((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}$')
AADHAR_CARD_REGEX = RegexValidator(r'^[-+]?[1-9]\d*$')


class Address(models.Model):
    aadhar = models.CharField(max_length=500, null=True)
    country = models.CharField(max_length=500, null=True)
    district = models.CharField(max_length=500, null=True)
    landmark = models.CharField(max_length=500, null=True, blank=True)
    house = models.CharField(max_length=500, null=True, blank=True)
    loc = models.CharField(max_length=500, null=True, blank=True)
    pc = models.CharField(max_length=500, null=True, blank=True)
    po = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=500, null=True, blank=True)
    subdistrict = models.CharField(max_length=500, null=True, blank=True)
    vtc = models.CharField(max_length=500, null=True, blank=True)


class User(AbstractUser):

    username = models.CharField(max_length=500, unique=True)
    email = models.EmailField(
        verbose_name='email address', null=True, blank=True)
    phone = models.CharField(max_length=500)
    lastModified = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=500, null=True)
    address = models.ForeignKey(
        to=Address, on_delete=models.PROTECT, blank=True, null=True)
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.username


class Audit(models.Model):
    client = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name='client1')
    introducer = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name="introducer1")
    message = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateField(auto_now_add=True)


class Request_Sent(models.Model):
    client = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name='request_client')
    introducer = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name="request_introducer")
    status = models.CharField(default="empty", max_length=10)


class Request_Confirm(models.Model):
    client = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name='client3')
    introducer = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name='introducer3')
    status = models.BooleanField(default=False)
    address = models.ForeignKey(
        to=Address, on_delete=CASCADE, related_name='address', null=True, blank=True)
    lastModified = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    passAttempt = models.IntegerField(default=0)
    addressAttempt = models.IntegerField(default=0)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
