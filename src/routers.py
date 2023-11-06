from django.urls import path, include

urlpatterns = [
    path('', include('src.exchange_rates.urls')),
    path('', include('src.users.urls')),
]
