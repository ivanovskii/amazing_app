from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from tutorial.quickstart.router import SwitchDetailRouter
from tutorial.quickstart.views import (
    UserViewSet,
    UserTweetsViewSet,
    TweetsViewSet,
    FollowViewSet,
    FeedViewSet,
    UserFollowsViewSet,
    UserFollowedViewSet,
    to_v1,
)
switch_router = SwitchDetailRouter()

router = ExtendedDefaultRouter()
user_route = router.register(r'users', UserViewSet)
user_route.register(r'tweets', UserTweetsViewSet, 'user-tweets', ['username'])
user_route.register(r'follows', UserFollowsViewSet, 'user-follows', ['username'])
user_route.register(r'followed', UserFollowedViewSet, 'user-followers', ['username'])
router.register(r'tweets', TweetsViewSet)
router.register(r'feed', FeedViewSet)
switch_router.register(r'follow', FollowViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', to_v1),
    path('v1/', include(switch_router.urls)),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]