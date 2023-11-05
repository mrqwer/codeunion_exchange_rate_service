from django.shortcuts import render
from rest_framework import generics
from .models import Currency
from .serializers import CurrencySerializer


class CurrencyList(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetail(generics.RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
