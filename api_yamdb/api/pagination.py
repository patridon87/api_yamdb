from rest_framework.pagination import PageNumberPagination


class TitlesPagination(PageNumberPagination):
    page_size = 20
