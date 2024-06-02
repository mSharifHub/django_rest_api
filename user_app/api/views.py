from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from user_app.api.serializers import RegistrationSerializer


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            token_message = 'token created' if token else 'token not created'
            return JsonResponse({
                'message': 'Registration successful',
                'username': user.username,
                'email': user.email,
                'token': token_message
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({"message": "some error occurred", "errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


