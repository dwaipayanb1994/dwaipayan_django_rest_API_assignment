from django.test import TestCase
from fetch_data.models import Metrics
import datetime

# Create your tests here.

class MetricsTestCase(TestCase):
    def success_and_test_blank_in_non_uniques(self):
        record = Metrics(place = 'test', date = datetime.date(1900, 1, 1))
        record.save()
        """ Duplication """
        # record.save()
    def test_blank_in_unique(self):
        """ Remove any parameter for testing """
        record = Metrics(place = 'tt', date = datetime.date(1900, 1, 1))
        record.save()
