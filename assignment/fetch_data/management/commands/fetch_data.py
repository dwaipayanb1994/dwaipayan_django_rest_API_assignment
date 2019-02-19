from django.core.management.base import BaseCommand
from fetch_data.models import Metrics
import requests
import datetime

class Command(BaseCommand):
    help = 'Fetch metrics from API'

    def handle(self, *args, **kwargs):
        locations = ['England', 'Scotland', 'Wales']
        metric_types = ['Tmax', 'Tmin', 'Rainfall']

        for location in locations:
            for param in metric_types:
                # Fetch every metric for each location
                url = 'https://s3.eu-west-2.amazonaws.com/interview-question-data/metoffice/{p}-{l}.json'.format(p = param, l = location)
                metrics = requests.get(url)

                for entry in metrics.json():
                    #if not present create else update
                    temp_date = datetime.date(entry['year'], entry['month'], 1)
                    if param == 'Tmax':
                        found = Metrics.objects.filter(place = location, date = temp_date).update(Tmax = entry['value'])
                    elif param == 'Tmin':
                        found = Metrics.objects.filter(place = location, date = temp_date).update(Tmin = entry['value'])
                    elif param == 'Rainfall':
                        found = Metrics.objects.filter(place = location, date = temp_date).update(Rainfall = entry['value'])
                    if not found:
                        if param == 'Tmax':
                            record = Metrics.objects.create(place = location, date = temp_date, Tmax = entry['value'])
                        elif param == 'Tmin':
                            record = Metrics.objects.create(place = location, date = temp_date, Tmin = entry['value'])
                        elif param == 'Rainfall':
                            record = Metrics.objects.create(place = location, date = temp_date, Rainfall = entry['value'])
