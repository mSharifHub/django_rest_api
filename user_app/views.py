from django.http import JsonResponse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # serialize the requested data
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # check if is valid
        serializer.is_valid(raise_exception=True)
        # get user value
        user = serializer.validated_data['user']
        # get or create token for user
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse(

            {
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
                 },
            status=status.HTTP_200_OK
        )
