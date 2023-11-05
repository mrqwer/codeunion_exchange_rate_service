from rest_framework.pagination import PageNumberPagination


class ExchangeRateViewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    page_query_param = 'page'
