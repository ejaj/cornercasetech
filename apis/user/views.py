from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status, generics
from rest_framework.decorators import action
from user.models import Employees
from user.serializers import (
    UserRegisterSerializer,
    EmployeeSerializer
)
import logging

logger = logging.getLogger(__name__)


class UserRegistrationAPIView(generics.GenericAPIView):
    """
    User Registration Api View.
    create:
    Create a new user instance.
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        """
        Handle post request
        :param request:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    """
    Logout Api View
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        """
        Handle post request
        :param request:
        :return:
        """
        try:
            refresh_token = self.request.data.get('refresh_token')
            if refresh_token == "all":
                tokens = OutstandingToken.objects.filter(user_id=request.user.id)
                for token in tokens:
                    t, _ = BlacklistedToken.objects.get_or_create(token=token)
                return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
            token = RefreshToken(token=refresh_token)
            token.blacklist()
            return Response({"status": "OK, goodbye"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class EmployeeModelViewSet(ModelViewSet):
    """
    retrieve:
    Return the given employee.
    list:
    Return a list of all the active existing employee.
    create:
    Create an new employee instance.
    update:
    Update an employee instance.
    delete:
    Delete an employee instance.
    """
    serializer_class = EmployeeSerializer
    queryset = Employees.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def perform_create(self, serializer):
        serializer.save(status="active", created=self.request.user, updated=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)

    @action(detail=True, methods=['patch'], )
    def status_update(self, request, *args, **kwargs):
        """
        Update employee status, active|banned
        """
        obj = self.get_object()
        employee_status = self.kwargs['status']
        obj.status = employee_status
        obj.save()
        serializer = EmployeeSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
