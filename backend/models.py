from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator

# Create your models here.

PHONE_NUMBER_REGEX = RegexValidator(
    r'^((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}$')
AADHAR_CARD_REGEX = RegexValidator(r'^[01]\d{3}[\s-]?\d{4}[\s-]?\d{4}$')


class User(AbstractUser):
    username = models.CharField(
        max_length=255, unique=True, auto_created=True)
    aadharNo = models.BigIntegerField(
        validators=[AADHAR_CARD_REGEX], unique=True, null=True)
    email = models.EmailField(
        verbose_name='email address', null=True, blank=True)
    phone = models.BigIntegerField(
        unique=True, null=True, blank=True, validators=[PHONE_NUMBER_REGEX])
    lastModified = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return str(self.name)


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
        to=User, on_delete=CASCADE, related_name='client2')
    introducer = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name="introducer2")
    status = models.BooleanField(default=False)


class Request_Confirm(models.Model):
    client = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name='client3')
    introducer = models.ForeignKey(
        to=User, on_delete=CASCADE, related_name='introducer3')
    status = models.BooleanField(default=False)
    adderss = models.CharField(max_length=255)
    lastModified = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255)
    passAttempt = models.IntegerField()
    addressAttempt = models.IntegerField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# class UserManager(BaseUserManager):
#     def create_user(self, email,name,year, password=None): #creates a normal user
#         if not email:
#             raise ValueError('Users must have an email address')
#         user = self.model(
#             email=self.normalize_email(email),
#             name = name,
#             year = year,
#         )
#         if year > 3:
#             user.admin = True
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self, email,name,year, password): #creates a staff user
#         user = self.create_user(
#             email,
#             password=password,
#             name = name,
#             year = year,
#         )
#         user.staff = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email,name,year, password): #creates a super user
#         """
#         Creates and saves a superuser with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             name = name,
#             year = year,
#         )
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user

# Model for custom user

# class User(AbstractBaseUser):
#     """
#         Custom user table for regestering the user
#         fields email , name , year , is_active , staff , admin

#     """
#  Default Django: eKYC
# OTP check to be made at frontend using status of eKYC api.
# Aadhar Number
# Email (null=True, blank=True)
# Phone Number (null=True, blank=True)
# Admin Right
# Last Modified (//can approve request only if!)
# Default Django First and Last Name
    # aadharNo = models.BigIntegerField(max=1000000000000,unique=True)
    # email = models.EmailField(verbose_name='email address')

    # name = models.CharField(max_length=40)
    # year = models.IntegerField()
    # is_active = models.BooleanField(default=True) #active status
    # staff = models.BooleanField(default=False)    #staff status
    # admin = models.BooleanField(default=False)    #admin status
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ["name","year"]

    # def get_full_name(self):
    #     return self.name

    # def get_short_name(self):
    #     return self.name

    # def __str__(self):
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True

    # @property                                     #property tag to call directly is staff
    # def is_staff(self):
    #     return self.staff

    # @property                                     #property tag to call directly is admin
    # def is_admin(self):
    #     return self.admin

    # objects = UserManager()

# model for adding a project


# class User(AbstractUser):
#     aadharNo = models.BigIntegerField(max=1000000000000,unique=True)
#     phoneNo = models.BigIntegerField(max=)
# from django.db import models
# from django.db.models.deletion import CASCADE
# from django.contrib.auth.models import AbstractUser, User
# from django.db.models.fields.related import ForeignKey
# from ckeditor.fields import RichTextField

# # imports for Token Authentications
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token

# # Create your models here.


# class AppUser(AbstractUser):
#     username = models.IntegerField(unique=True)
#     name = models.CharField(max_length=255)
#     admin = models.BooleanField(default=False)
#     disabled = models.BooleanField(default=False)

#     def __str__(self) -> str:
#         return str(self.username)


# class Project(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     wiki = RichTextField()
#     date_started = models.DateField(auto_now_add=True)
#     team_members = models.ManyToManyField(
#         AppUser, related_name='team_member')
#     creator = models.ManyToManyField(AppUser, related_name='maintainer'
#     def __str__(self) -> str:
#         return self.name


# class List(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     project = models.ForeignKey(to=Project, on_delete=CASCADE)

#     def __str__(self) -> str:
#         return self.name


# class Card(models.Model):
#     title = models.CharField(max_length=255, unique=True)
#     description = RichTextField()
#     complete = models.BooleanField(default=False)
#     assignee = models.ManyToManyField(AppUser, related_name='Assignees')
#     list = models.ForeignKey(to=List, on_delete=CASCADE)
#     due_date = models.DateField(null=True, blank=True)

#     def __str__(self) -> str:
#         return self.title


# class Comment(models.Model):
#     user = models.ForeignKey(to=AppUser, on_delete=CASCADE)
#     message = models.CharField(max_length=255)
#     card = models.ForeignKey(to=Card, on_delete=CASCADE)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# class Request_Sent(models.Model):
#     Request_Sent =
