from optparse import make_option
import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from src.exchange_rates.models import Currency  # Replace 'yourapp' with your app's name
from enum import Enum
from typing import Optional, Union


class Fields(str, Enum):
    CURRENCY_ID = "currency_id"
    CURRENCY_NAME = "currency_name"
    CURRENCY_VALUE = "currency_value"


CURRENCIES = ['AUD', 'AZN', 'AMD', 'BYN', 'BRL', 'HUF', 'HKD', 'GEL', 'DKK', 'AED', 'USD', 'EUR', 'INR', 'IRR', 'CAD',
              'CNY', 'KWD', 'KGS', 'MYR', 'MXN', 'MDL', 'NOK', 'PLN', 'SAR', 'RUB', 'XDR', 'SGD', 'TJS', 'THB', 'TRY',
              'UZS', 'UAH', 'GBP', 'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY']


class Behaviour(str, Enum):
    SHOW = "get"
    SHOW_SHORT = "g"
    STORE = "store"
    STORE_SHORT = "s"


class Command(BaseCommand):
    help = """
    Update exchange rates from XML source
    
    """

    @staticmethod
    def custom_validation(field, values) -> Union[Union[str, int], None]:
        if field == Fields.CURRENCY_ID:
            filtered_ids = list(filter(lambda n: n < 1 or n > 39, values))
            if filtered_ids:
                return filtered_ids[0]
        elif field == Fields.CURRENCY_NAME:
            filtered_names = list(filter(lambda name: name not in CURRENCIES, values))
            if filtered_names:
                return filtered_names[0]

    def add_arguments(self, parser):
        parser.add_argument('--' + Fields.CURRENCY_ID, nargs='+', type=int, help='Currency ID (1 to 39)')
        parser.add_argument('--' + Fields.CURRENCY_NAME, nargs='+', type=str, help='Currency Name (e.g., AUD)')
        parser.add_argument('--' + Fields.CURRENCY_VALUE, nargs='+', type=str, help='Currency value to set')
        parser.add_argument('-' + Behaviour.SHOW_SHORT, '--' + Behaviour.SHOW, action='store_true',
                            help="To get the currency or currencies")
        parser.add_argument('-' + Behaviour.STORE_SHORT, '--' + Behaviour.STORE, action="store_true",
                            help="To store or to update the currencies")

    def handle(self, *args, **kwargs):
        currency_ids = kwargs[Fields.CURRENCY_ID]
        currency_names = kwargs[Fields.CURRENCY_NAME]
        currency_values = kwargs[Fields.CURRENCY_VALUE]
        show_data = kwargs[Behaviour.SHOW]
        store_data = kwargs[Behaviour.STORE]

        if currency_ids:
            c_id = self.custom_validation(Fields.CURRENCY_ID, currency_ids)
            if c_id:
                self.stdout.write(self.style.NOTICE(f"Currency with id {c_id} does not exist"))
        elif currency_names:
            currency_names = list(map(lambda name: name.upper(), currency_names))
            c_name = self.custom_validation(Fields.CURRENCY_NAME, currency_names)
            if c_name:
                self.stdout.write(self.style.NOTICE(f"Currency with name {c_name} does not exist"))

        if show_data and store_data:
            self.stdout.write(self.style.NOTICE("You cannot update and get the currencies at the same time"))
        elif show_data:
            if currency_values:
                self.stdout.write(self.style.NOTICE(
                    f"There is no need to provide values with -{Behaviour.SHOW_SHORT}, --{Behaviour.SHOW}"))

            if currency_ids:
                currency_ids_unique = list(set(c_id for c_id in currency_ids))
                currencies = Currency.objects.filter(id__in=currency_ids_unique)
            elif currency_names:
                currency_names_unique = list(set(c_name for c_name in currency_names))
                currencies = Currency.objects.filter(name__in=currency_names_unique)
            else:
                currencies = Currency.objects.all()
            if not currencies:
                self.stdout.write(
                    self.style.SUCCESS("There is no data in database. Firstly, update the currencies in database"))
                return
            print("ID    NAME    RATE")
            for currency in currencies:
                print(currency.id, "     ", currency.name, "     ", currency.rate)
            self.stdout.write(self.style.SUCCESS("Successfully displayed"))

        elif store_data:
            if currency_ids:
                if len(currency_ids) != len(currency_values):
                    self.stdout.write(
                        self.style.NOTICE("Currency ids and currency values lists should be equal length"))
                    return
                if len(currency_ids) != len(set(currency_ids)):
                    self.stdout.write(self.style.NOTICE(
                        "Please, with 'store' behaviour, there should not be duplicates in 'id' list"))
                    return
                for c_id, rate in zip(currency_ids, currency_values):
                    currency = Currency.objects.get(pk=c_id)
                    currency.rate = rate
                    currency.save()
                self.stdout.write(self.style.SUCCESS("IDs and corresponding rate values are saved successfully"))
                return
            elif currency_names:
                if len(currency_names) != len(currency_values):
                    self.stdout.write(
                        self.style.NOTICE("Currency ids and currency values lists should be equal length"))
                    return
                if len(currency_names) != len(set(currency_names)):
                    self.stdout.write(self.style.NOTICE(
                        "Please, with 'store' behaviour, there should not be duplicates in 'names' list"))
                    return
                for c_name, rate in zip(currency_names, currency_values):
                    currency = Currency.objects.get(name=c_name)
                    currency.rate = rate
                    currency.save()
                self.stdout.write(self.style.SUCCESS("Names and corresponding rate values are saved successfully"))
                return
            if currency_values:
                self.stdout.write(self.style.NOTICE("There are no name or id lists"))
                return
            xml_url = 'http://www.nationalbank.kz/rss/rates_all.xml'
            response = requests.get(xml_url)
            if response.status_code == 200:
                xml_data = response.content
                root = ET.fromstring(xml_data)

                for item in root.findall('.//item'):
                    currency_name = item.find('title').text
                    currency_rate = item.find('description').text

                    currency_obj, created = Currency.objects.get_or_create(name=currency_name, defaults={'rate': 0})

                    if not created:
                        currency_obj.rate = currency_rate
                        currency_obj.save()

                self.stdout.write(self.style.SUCCESS('Successfully updated exchange rates'))
            else:
                self.stdout.write(self.style.ERROR('Failed to fetch exchange rates'))
        else:
            self.print_help("manage.py", 'update_currency')
