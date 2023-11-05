import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from src.exchange_rates.models import Currency


class Command(BaseCommand):
    help = 'Update exchange rates from XML source'

    def handle(self, *args, **options):
        xml_url = 'http://www.nationalbank.kz/rss/rates_all.xml'
        response = requests.get(xml_url)
        print("Hello")
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
