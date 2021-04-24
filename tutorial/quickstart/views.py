from django.contrib.auth.models import User
from tutorial.quickstart.models import Tweet, Follow

from django.shortcuts import redirect

from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
    ModelViewSet,
    GenericViewSet,
)

from tutorial.quickstart.serializers import (
    UserSerializer,
    TweetSerializer,
    FollowSerializer,
    UserFollowsSerializer,
    UserFollowedSerializer,
)

from tutorial.quickstart.permissons import IsTweetAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)


class UserViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'


class TweetsViewSet(ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsTweetAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ​/users​/{username}​/tweets​/
class UserTweetsViewSet(ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(
            author__username=self.kwargs['parent_lookup_username'])


# POST, DELETE follow/{username}
class FollowViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Follow.objects
    serializer_class = FollowSerializer
    lookup_field = 'follower'

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follows=User.objects.get(username=self.kwargs[self.lookup_field])
        serializer.save(follower=self.request.user, follows=follows)

    def get_object(self):
        return self.queryset.filter(
            follower=self.request.user,
            follows__username=self.kwargs[self.lookup_field],
        )


class FeedViewSet(ListModelMixin, GenericViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            author__followers__follower=self.request.user # В его фолловерах находимся мы
        )


class UserFollowsViewSet(ListModelMixin, GenericViewSet):
    queryset = Follow.objects
    serializer_class = UserFollowsSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follower__username=username)


class UserFollowedViewSet(ListModelMixin, GenericViewSet):
    queryset = Follow.objects
    serializer_class = UserFollowedSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follows__username=username)


def to_v1(request):
    return redirect('v1/')