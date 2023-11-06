from rest_framework import generics, permissions
from rest_framework.decorators import authentication_classes, permission_classes
from .models import Currency
from .serializers import CurrencySerializer
from .pagination import ExchangeRateViewPagination


class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ExchangeRateViewPagination


class CurrencyDetail(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencySerializer
