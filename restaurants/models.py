from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models
from user.models import Employees

# Create your models here.
UserModel = get_user_model()


class Vote(models.Model):
    voted_by = models.ForeignKey(Employees, verbose_name=_('Employee'), related_name='voted_employee',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Restaurants(models.Model):
    """
    Stores a single restaurant entry, related to :model:`user.User`.
    """
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)

    status = models.CharField(_('Status'), max_length=100, null=True, blank=True)
    created = models.ForeignKey(UserModel, verbose_name=_('Created User'), related_name='restaurant_created',
                                on_delete=models.SET_NULL, null=True, blank=True)
    updated = models.ForeignKey(UserModel, verbose_name=_('Updated User'), related_name='restaurant_updated',
                                on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        db_table = 'restaurants'

    def __str__(self):
        return self.name


class RestaurantMenu(models.Model):
    """
    Stores a single restaurant menu entry, related to :model:`user.User` and :model:`restaurants.Restaurants`.
    """
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurants, verbose_name=_('Restaurant'), related_name='restaurant_menu',
                                   on_delete=models.CASCADE)
    date = models.DateField(_('Date'), null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(_('Status'), max_length=100, null=True, blank=True)
    created = models.ForeignKey(UserModel, verbose_name=_('Created User'), related_name='restaurant_menu_created',
                                on_delete=models.SET_NULL, null=True, blank=True)
    updated = models.ForeignKey(UserModel, verbose_name=_('Updated User'), related_name='restaurant_menu_updated',
                                on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(Vote, related_query_name='voted_restaurant_menu')

    class Meta:
        ordering = ['-updated_at']
        db_table = 'restaurant_menu'
        indexes = [models.Index(fields=['date'])]
        unique_together = ('name', 'restaurant', 'date',)

    def __str__(self):
        return self.name


class WinnerRestaurant(models.Model):
    """
    Stores a single winner restaurant entry, related to :model:`user.User` and :model:`restaurants.Restaurants`.
    """

    restaurant = models.ForeignKey(Restaurants, verbose_name=_('Restaurant'), related_name='winner_restaurant',
                                   on_delete=models.CASCADE)
    date = models.DateField(_('Date'), null=True, blank=True)
    total_vote = models.PositiveIntegerField()

    class Meta:
        ordering = ['-total_vote']
        db_table = 'winner_restaurant'
        indexes = [models.Index(fields=['date'])]
        unique_together = ('restaurant', 'date')

    def __str__(self):
        return str(self.restaurant)
