from rest_framework import generics
from rest_framework.decorators import authentication_classes, permission_classes
from .models import Currency
from .serializers import CurrencySerializer
from .pagination import ExchangeRateViewPagination


@authentication_classes('rest_framework_simplejwt.authentication.JWTAuthentication')
@permission_classes('rest_framework.permissions.IsAuthenticated')
class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = ExchangeRateViewPagination

@authentication_classes('rest_framework_simplejwt.authentication.JWTAuthentication')
@permission_classes('rest_framework.permissions.IsAuthenticated')
class CurrencyDetail(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
