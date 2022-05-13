from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from . import managers


class User(AbstractBaseUser, PermissionsMixin):
    """
    Stores a single user entry.
    """
    email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField(_('Name'), max_length=30, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Active'), default=False)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
    about = models.TextField(_('About'), null=True, blank=True)
    objects = managers.UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.email

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()


class Employees(models.Model):
    """
    Stores a single employee entry, related to :model:`user.User`.
    """
    name = models.CharField(max_length=100, null=True)
    employee_id = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=200, null=True)
    status = models.CharField(_('Status'), max_length=100, null=True, blank=True)
    created = models.ForeignKey(User, verbose_name=_('Created User'), related_name='employee_created',
                                on_delete=models.SET_NULL, null=True, blank=True)
    updated = models.ForeignKey(User, verbose_name=_('Updated User'), related_name='employee_updated',
                                on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        db_table = 'employees'
        indexes = [models.Index(fields=['status'])]

    def __str__(self):
        return self.name
