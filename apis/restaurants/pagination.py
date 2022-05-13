from rest_framework.pagination import LimitOffsetPagination


class RestaurantPagination(LimitOffsetPagination):
    def __init__(self):
        self.default_limit = 20
        super(RestaurantPagination, self).__init__()
