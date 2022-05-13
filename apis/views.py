from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import views


class HelloApiView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        print(self.request.user.id)
        content = {'message': 'Hello, World!'}
        return Response(content)
