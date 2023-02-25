import csv
from pprint import pprint
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
import urllib.parse


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    bus_stops_list = []
    with open('pagination/data-398-2018-08-30.csv', newline='', encoding='cp1251') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop_line = {
                'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
            bus_stops_list.append(stop_line)

    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(bus_stops_list, 10)
    current_page = paginator.get_page(page_number)
    objects_on_page = current_page.object_list
    next_page_url = f'{reverse(bus_stations)}?{urllib.parse.urlencode({"page": current_page})}'

    if current_page.has_next():
        next_page_params = {'page': current_page.next_page_number()}
        params = urllib.parse.urlencode(next_page_params)
        next_page_url = f'{reverse(bus_stations)}?{params}'

    prev_page_url = f'{reverse(bus_stations)}?{urllib.parse.urlencode({"page": current_page})}'

    if current_page.has_previous():
        prev_page_params = {'page': current_page.previous_page_number()}
        params = urllib.parse.urlencode(prev_page_params)
        prev_page_url = f'{reverse(bus_stations)}?{params}'

    context = {
        'bus_stations': objects_on_page,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }

    return render(request, 'index.html', context)
