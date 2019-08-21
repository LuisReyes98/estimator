from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as translate
from estimator.mixins import TimeStampFields

# Modelos para el control de usuarios


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AppUser(AbstractUser, TimeStampFields):
    """Basic User model."""

    username = None  # removiendo campo username

    # campo unico email  de registro
    email = models.EmailField(translate('Email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        pass

    @property
    def full_name(self):
        """Retorna el nombre completo del usuario"""
        return '%s %s' % (self.first_name, self.last_name)


class Company(TimeStampFields):
    """ Company user model """
    # Referencias
    user = models.OneToOneField(
        AppUser,
        verbose_name=translate('User'),
        on_delete=models.CASCADE,
        parent_link=True
    )

    # Campos propios
    company_name = models.CharField(
        translate('Name of the company'),
        max_length=50,
        blank=False
    )

    def __str__(self):
        # Retornar el nombre de la compañia
        return self.company_name

    class Meta:
        verbose_name = translate("Company")
        verbose_name_plural = translate("Companies")


class CompanyUser(TimeStampFields):
    """ Company User model user model """
    # Referencias
    user = models.OneToOneField(  # Autenticacion de usuario
        AppUser,
        verbose_name=translate('User'),
        on_delete=models.CASCADE,
        parent_link=True
    )

    company = models.ForeignKey(  # Compañia a la que pertenece
        Company,
        verbose_name=translate('Company'),
        on_delete=models.CASCADE,
        parent_link=True,
        blank=False,
        null=False,
    )

    def __str__(self):
        # Retornar el nombre de la compañia y nombre del usuario
        return '%s: %s' % (self.company.company_name, self.user.username)

    class Meta:
        verbose_name = translate("Company User")
        verbose_name_plural = translate("Company Users")
