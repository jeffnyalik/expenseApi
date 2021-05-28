from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response({"custom_key": "custom message"}, status=401)

    # else
    # default case
    return exception_handler(exc, context)