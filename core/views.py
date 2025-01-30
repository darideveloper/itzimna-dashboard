from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.serializers import (
    CustomTokenObtainPairSerializer,
    CustomTokenRefreshSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class ValidateRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        
        # Auto response to manage auth with drf
        return Response(
            {
                "status": "ok",
                "message": "Token is valid",
                "data": {}
            },
            status=status.HTTP_200_OK
        )