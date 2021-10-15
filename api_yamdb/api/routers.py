from rest_framework import routers


class MeRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'',
            mapping={'get': 'retrieve', 'patch': "partial_update"},
            name='{basename}-detail',
            initkwargs={},
            detail=False
        )
    ]
