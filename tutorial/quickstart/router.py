from rest_framework.routers import SimpleRouter, Route

class SwitchDetailRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'post': 'create',
                'delete': 'destroy'
            },
            name='{basename}-switch',
            detail=True,
            initkwargs={'suffix': 'Switch'}
        ),
    ]
