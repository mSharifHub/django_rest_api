import logging
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                'error': "Unauthorized access. Please provide valid credentials.",
                'method': context['request'].method,
                'url': context['request'].build_absolute_uri(),
            }
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                'error': "Forbidden access. You don not have permission to perform this operation:"
                         f" {context['request'].method}. {context['request'].build_absolute_uri()}"
            }
        logger.error(f"error: {response.data}, Status Code: {response.status_code}")
    else:
        if isinstance(exc, NotAuthenticated):
            response = Response(
                {
                    'error': 'Authentication credentials were not provided.',
                    'method': context['request'].method,
                    'url': context['request'].build_absolute_uri(),
                }
            )
    return response
