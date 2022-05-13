from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from apis.restaurants.pagination import RestaurantPagination
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from user.models import Employees

from restaurants.models import (
    Restaurants,
    RestaurantMenu,
    WinnerRestaurant
)
from restaurants.serializers import (
    RestaurantSerializer,
    RestaurantMenuSerializer,
    RestaurantMenVoteResultSerializer
)
from datetime import datetime, timedelta
import logging

logger = logging.getLogger()


class RestaurantModelViewSet(ModelViewSet):
    """
    retrieve:
    Return the given restaurant.
    list:
    Return a list of all the active existing restaurant.
    create:
    Create a new restaurant instance.
    update:
    Update a restaurant instance.
    delete:
    Delete a restaurant instance.
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurants.objects.filter(status="active")
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(status="active", created=self.request.user, updated=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)


class RestaurantMenuModelViewSet(ModelViewSet):
    """
    retrieve:
    Return the given restaurant menu.
    list:
    Return a list of all the active existing restaurant menu.
    create:
    Create a new restaurant menu instance.
    update:
    Update a restaurant menu instance.
    """
    serializer_class = RestaurantMenuSerializer
    pagination_class = RestaurantPagination
    queryset = RestaurantMenu.objects.filter(status="active")
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant', 'date', 'price']
    http_method_names = ['get', 'post', 'put']

    def perform_create(self, serializer):
        serializer.save(status="active", created=self.request.user, updated=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)

    @action(detail=True, methods=['post'])
    def vote(self, request, *args, **kwargs):
        """
        Give a vote by an employee restaurant menu
        """
        try:
            menu = self.get_object()
            employee = get_object_or_404(Employees, pk=request.data.get('employee_pk'))
            menu.votes.get_or_create(voted_by=employee)
            msg = {'detail': "voted success"}
            return Response(msg, status=status.HTTP_200_OK)
        except (IntegrityError, Exception) as e:
            msg = {'detail': str(e)}
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def today_result(self, request, *args, **kwargs):
        """
        Today result, regarding employee vote on restaurant menu.
        """
        try:
            current_date = datetime.now().date()
            yesterday = datetime.now() - timedelta(1)
            yesterday_date = yesterday.date()

            result = RestaurantMenu.objects.filter(date=current_date).annotate(
                vote_count=Count('votes')
            ).order_by('-vote_count')
            if result and result[0].vote_count > 0:
                # Store winner restaurant, for calculating winner restaurant cross 3 consecutive date
                obj, created = WinnerRestaurant.objects.update_or_create(
                    restaurant=result[0].restaurant, date=current_date, total_vote=result[0].vote_count,
                    defaults={'total_vote': result[0].vote_count},
                )

                winner_count = WinnerRestaurant.objects.filter(restaurant=result[0].restaurant,
                                                               date__in=[current_date, yesterday_date]).count()
                if winner_count < 3:
                    winner = result
                else:
                    winner = result.exclude(restaurant=result[0].restaurant)
            else:
                winner = result
            serializer = RestaurantMenVoteResultSerializer(winner, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (IntegrityError, Exception) as e:
            msg = {'detail': str(e)}
            logger.error(msg)
            return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
