from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from .models import *


class IsTweetAuthorOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj: Tweet):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            obj.author == request.user
        )
