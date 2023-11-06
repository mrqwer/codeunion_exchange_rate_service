from django.test import TestCase
from src.exchange_rates.models import Currency


class CurrencyModelTestCase(TestCase):
    def setUp(self):
        Currency.objects.create(name="USD", rate=1.0)
        Currency.objects.create(name="EUR", rate=0.85)
        Currency.objects.create(name="GBP", rate=0.75)
        Currency.objects.create(name="AUD", rate=1.2)
        Currency.objects.create(name="JPY", rate=110.0)

    def test_currency_name(self):
        usd = Currency.objects.get(name="USD")
        eur = Currency.objects.get(name="EUR")
        gbp = Currency.objects.get(name="GBP")
        aud = Currency.objects.get(name="AUD")
        jpy = Currency.objects.get(name="JPY")

        self.assertEqual(usd.__str__(), "USD")
        self.assertEqual(eur.__str__(), "EUR")
        self.assertEqual(gbp.__str__(), "GBP")
        self.assertEqual(aud.__str__(), "AUD")
        self.assertEqual(jpy.__str__(), "JPY")

    def test_currency_rate(self):
        usd = Currency.objects.get(name="USD")
        eur = Currency.objects.get(name="EUR")
        gbp = Currency.objects.get(name="GBP")
        aud = Currency.objects.get(name="AUD")
        jpy = Currency.objects.get(name="JPY")

        self.assertEqual(float(usd.rate), 1.0)
        self.assertEqual(float(eur.rate), 0.85)
        self.assertEqual(float(gbp.rate), 0.75)
        self.assertEqual(float(aud.rate), 1.2)
        self.assertEqual(float(jpy.rate), 110.0)
