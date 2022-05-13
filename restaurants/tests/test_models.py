from django.test import TestCase
from restaurants.models import Restaurants, RestaurantMenu, WinnerRestaurant
import datetime


class TestModels(TestCase):
    def setUp(self):
        self.restaurant = Restaurants.objects.create(
            name="Kazi",
            location='Madaripur',
            status='active'
        )
        self.menu = RestaurantMenu.objects.create(
            name="Pizza",
            restaurant_id=self.restaurant.pk,
            date=datetime.date.today(),
            price=20.3,
            status='active'
        )
        self.winner_restaurant = WinnerRestaurant.objects.create(
            restaurant_id=self.restaurant.pk,
            date=datetime.date.today(),
            total_vote=20
        )

    def test_restaurant_name_location(self):
        self.assertEqual(self.restaurant.name, 'Kazi')
        self.assertEqual(self.restaurant.location, 'Madaripur')

    def test_restaurant_menu(self):
        self.assertEqual(self.menu.restaurant_id, self.restaurant.pk)

    def test_restaurant_result(self):
        self.assertEqual(self.winner_restaurant.date, datetime.date.today())
