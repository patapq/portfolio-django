from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup


def index(request):

    st_accept = 'text/html'
    st_useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'

    headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent
    }

    from datetime import datetime

    current_week = datetime.now().isocalendar()[1]
    start_week = datetime.now().replace(month=9, day=1).isocalendar()[1]
    week = current_week - start_week + 1


    req = requests.get(f'https://eners.kgeu.ru/apish2.php?group=ПИ-1-21&week={week}&type=one', headers)
    src = req.text

    soup = BeautifulSoup(src, 'html.parser')
    days = soup.findAll('div', class_='card')

    context = {'days': []}
    for day in days:
        day_info = {'day_name': day.a.string.strip(), 'items': []}
        items = day.select('.list-group-item')
        for k, item in enumerate(items):
            time = '-'.join(item.select_one('.col-sm-2').text.strip().split(' '))
            subject = item.select_one('.col-sm-6').text.strip()
            cabinet = item.select_one('.col-sm-4 .tx-normal').text.strip()
            instructor = item.select_one('.col-sm-4 .text-muted').text.strip()

            item_info = {
                'index': k + 1,
                'time': time,
                'subject': subject,
                'cabinet': cabinet,
                'instructor': instructor
            }

            day_info['items'].append(item_info)
        context['days'].append(day_info)

    return render(request, 'info/index.html', context)