from fetch_data.models import Metrics

import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


""" Create the output """

def Tmax_output(records):
    output = '['
    for record in records:
        if record.Tmax:
            output += "'{date}':{value}, ".format(date = str(record.date)[:7], value = str(record.Tmax))
    output = output[:-2] + ']'
    return output
def Tmin_output(records):
    output = '['
    for record in records:
        if record.Tmin:
            output += "'{date}':{value}, ".format(date = str(record.date)[:7], value = str(record.Tmin))
    output = output[:-2] + ']'
    return output
def Rainfall_output(records):
    output = '['
    for record in records:
        if record.Rainfall:
            output += "'{date}':{value}, ".format(date = str(record.date)[:7], value = str(record.Rainfall))
    output = output[:-2] + ']'
    return output

# Create your views here.
def validate_date(date):
    if len(date) == 6 and date.isdigit() and 0 < int(date[:2]) < 13 and int(date[2:]) > 0:
        return True
    return False

@api_view(['GET'])
def handle_get(request):
    if request.method != 'GET':
        return Response('', status=status.HTTP_400_BAD_REQUEST)

    """ Get API parameters """

    date_from = request.GET.get('from', None)
    date_to = request.GET.get('to', None)
    metric = request.GET.get('metric', None)
    location = request.GET.get('location', None)

    locations = ['England', 'Scotland', 'Wales']
    metric_types = ['Tmax', 'Tmin', 'Rainfall']

    """ Validate API parameter """

    if location not in locations:
        return Response('Invalid location', status=status.HTTP_400_BAD_REQUEST)
    elif metric not in metric_types:
        return Response('Invalid metric', status=status.HTTP_400_BAD_REQUEST)
    elif not validate_date(date_from):
        return Response('Invalid from date', status=status.HTTP_400_BAD_REQUEST)
    elif not validate_date(date_to):
        return Response('Invalid to date', status=status.HTTP_400_BAD_REQUEST)
    else:
        d_f = datetime.date(int(date_from[2:]), int(date_from[:2]), 1)
        d_t = datetime.date(int(date_to[2:]), int(date_to[:2]), 1)
        if d_f > d_t:
            return Response('Logically incorrect dates', status=status.HTTP_400_BAD_REQUEST)
        queryset = Metrics.objects.filter(place = location, date__range = (d_f, d_t)).order_by('date')

        metric_to_function = {'Tmax':Tmax_output, 'Tmin':Tmin_output, 'Rainfall':Rainfall_output}
        if queryset:
            return Response(metric_to_function[metric](queryset), status=status.HTTP_200_OK)
        else:
            return Response('No data found', status=status.HTTP_400_BAD_REQUEST)
