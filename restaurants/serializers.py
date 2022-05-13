from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

from restaurants.models import Restaurants, RestaurantMenu

UserModel = get_user_model()


class RestaurantSerializer(serializers.ModelSerializer):
    """
    A Serializer class for a Restaurant
    """
    name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Restaurants.objects.all())]
    )

    class Meta:
        model = Restaurants
        fields = ['id', 'name', 'location', 'status']


class RestaurantMenuSerializer(serializers.ModelSerializer):
    """
    A Serializer class for a Restaurant
    """
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurants.objects.filter(status="active"),
                                                    required=True, write_only=True)
    date = serializers.DateField(required=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
    restaurant_detail = serializers.SerializerMethodField()

    @staticmethod
    def get_restaurant_detail(obj):
        restaurant = obj.restaurant
        serializer = RestaurantSerializer(restaurant)
        return serializer.data

    class Meta:
        model = RestaurantMenu
        fields = ['id', 'name', 'price', 'date', 'status', 'restaurant', 'restaurant_detail']
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_id', 'updated_id', 'restaurant_detail')


class RestaurantMenVoteResultSerializer(RestaurantMenuSerializer):
    total_vote = serializers.SerializerMethodField()

    @staticmethod
    def get_total_vote(obj):
        return obj.vote_count

    class Meta:
        model = RestaurantMenu
        fields = RestaurantMenuSerializer.Meta.fields + [
            'total_vote'
        ]
        read_only_fields = fields
