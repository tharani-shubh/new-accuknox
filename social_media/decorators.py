from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from social_media.models import Member


def verify_member(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        """
        Decorator to check if member with given pk exists, if not return error response
        """
        pk = kwargs.pop('pk')
        try:
            member = Member.objects.get(id=pk)
        except Member.DoesNotExist:
            return Response({"message": f"No member with id - {pk} exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        return func(request, member, *args, **kwargs)
    return wrapper