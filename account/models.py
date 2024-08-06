from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin,AbstractBaseUser
from django.utils import timezone



class UserManager(BaseUserManager):
    def _create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('L\'adresse e-mail doit etre spécifiée.')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)

        return self._create_user(email,password)
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    firstName = models.CharField( ("first name"), max_length=150)
    lastName = models.CharField(("last name"), max_length=150, blank=True)
    email = models.EmailField(("email address"), unique = True)
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(("date joined"), default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName","lastName"]

    class Role(models.TextChoices):
        PARENT = "PARENT","parent"
        ADMIN = "ADMIN","admin"

    role =models.CharField(max_length=32,choices=Role.choices,default='')

class AmdinManager(models.Manager):
    def get_queryset(self,*arg,**kwargs) -> models.QuerySet:
        return super().get_queryset(*arg,**kwargs).filter(role=CustomUser.Role.ADMIN)

class ParentManager(models.Manager):
    def get_queryset(self,*arg,**kwarg) -> models.QuerySet:
        return super().get_queryset(*arg,**kwarg).filter(role=CustomUser.Role.PARENT)

class Admin(CustomUser):
    class Meta:
        proxy=True
    
    def save(self,*arg,**kwargs):
        if not self.pk:
            self.role =CustomUser.Role.ADMIN
        return super().save(*arg,**kwargs)

class Parent(CustomUser):
    class Meta:
        proxy=True
    
    def save(self,*arg,**kwargs):
        if not self.pk:
            self.role =CustomUser.Role.PARENT
        return super().save(*arg,**kwargs)
