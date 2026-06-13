from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('owner', 'Administrateur'),
        ('manager', 'Gérant'),
        ('cashier', 'Caissier'),
        ('seller', 'Vendeur'),
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='seller')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True, null=True)

    created_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_users'
    )


    store = models.ForeignKey(
        "stores.Store",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='stores_users'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.store}({self.role})"

    def is_owner(self):
        return self.role == 'owner'

    def get_collaborators(self):
        if self.role == 'platform_admin':
            return CustomUser.objects.filter(created_by=self, role='owner')

        if self.role == 'owner':
            return CustomUser.objects.filter(
                created_by=self,
                role__in=['manager', 'cashier', 'seller']
            )

        return CustomUser.objects.none()