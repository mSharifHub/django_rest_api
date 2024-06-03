from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from user_app.api.serializers import RegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return JsonResponse({
                'message': 'Registration successful',
                'username': user.username,
                'email': user.email,
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({"message": "some error occurred", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def logout_view(request):
#     if request.method == 'POST':
#         token = request.user.auth_token.delete()
#         return JsonResponse({'message': 'logged out successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout_view(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return JsonResponse({'message': "logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as err:
        return JsonResponse({'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
