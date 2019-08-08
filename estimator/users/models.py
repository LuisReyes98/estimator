from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as translate
# Create your models here.


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


class AppUser(AbstractUser):
    """Basic User model."""

    username = None
    email = models.EmailField(translate('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        """Retorna el nombre completo del usuario"""
        return '%s %s' % (self.first_name, self.last_name)


class Company(models.Model):
    """ Company user model """
    # Referencias
    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        parent_link=True
    )

    # Campos propios
    company_name = models.CharField(
        translate('name of company'),
        max_length=30,
        blank=False
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Retornar el nombre de la compañia
        return self.company_name


class CompanyUser(models.Model):
    """ Company User model user model """
    # Referencias
    user = models.OneToOneField(  # Autenticacion de usuario
        AppUser,
        on_delete=models.CASCADE,
        parent_link=True
    )

    company = models.ForeignKey(  # Compañia a la que pertenece
        Company,
        on_delete=models.CASCADE,
        parent_link=True,
        blank=False,
        null=False,
    )
    # Campos propios
    is_manager = models.BooleanField(
        translate('is manager'),
        default=False,
        null=False
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Retornar el nombre de la compañia y nombre del usuario
        return '%s: %s' % (self.company.company_name, self.user.username)
