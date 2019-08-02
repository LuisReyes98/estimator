from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
# Create your models here.


class Company(AbstractBaseUser, PermissionsMixin):
    """Company model"""
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=30, blank=False)
    user_name = models.CharField(max_length=30, blank=False)
    full_name = models.CharField(max_length=30, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'company_name',
        'full_name',
    ]

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def get_full_name(self):
        return self.full_name

    def get_user_name(self):
        return self.user_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class CompanyManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
        """
        Guarda al usuario con email y contraseña
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Guarda al super usuario con email y contraseña
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



    # def _create_user(self, email, password, **extra_fields):
    #     """
    #     Creates and saves a User with the given email and password.
    #     """
    #     if not email:
    #         raise ValueError('The given email must be set')
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_user(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, email, password, **extra_fields):
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self._create_user(email, password, **extra_fields)