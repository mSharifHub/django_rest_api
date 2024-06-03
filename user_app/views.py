from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializers import CustomTokenObtainSerializer


class CustomAuthToken(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)

        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return JsonResponse({
            'token': tokens['access'],
            'refresh': tokens['refresh'],
            'user_id': user.pk,
            'username': user.username,
        }, status=status.HTTP_200_OK)
