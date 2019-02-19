from fetch_data.models import Metrics
from GET_API.views import Tmax_output, Tmin_output, Rainfall_output
from django.test import TestCase, Client
import datetime

# tests for views

class API_Test(TestCase):
    """ Test module for GET all puppies API """
    client = Client()
    def setUp(self):
        Metrics.objects.create(place = 'England', date = datetime.date(2011, 1, 1), Tmax = 11.1, Tmin = 0.1, Rainfall = 15)
        Metrics.objects.create(place = 'England', date = datetime.date(2012, 3, 1), Tmax = 19.2, Tmin = 1, Rainfall = 5)
        Metrics.objects.create(place = 'Scotland', date = datetime.date(2013, 5, 1), Tmax = 46.6, Tmin = 3.8, Rainfall = 34.7)
        Metrics.objects.create(place = 'England', date = datetime.date(2014, 6, 1), Tmax = 5.7, Tmin = 1.6, Rainfall = 45.7)
        Metrics.objects.create(place = 'Scotland', date = datetime.date(2018, 2, 1), Tmax = 34.1, Tmin = 4.1, Rainfall = 18.3)
        Metrics.objects.create(place = 'England', date = datetime.date(2019, 12, 1), Tmax = 23.9, Tmin = 3.5, Rainfall = 11.1)

    def test_get_Tmax(self):
        # get API response
        response = self.client.get('/api/?location=England&metric=Tmax&from=012010&to=092018')
        # get data from db
        location = 'England'
        d_f = datetime.date(2010,1,1)
        d_t = datetime.date(2018,9,1)
        filtered_output = Metrics.objects.filter(place = location, date__range = (d_f, d_t)).order_by('date')

        self.assertEqual(response.data, Tmax_output(filtered_output))
