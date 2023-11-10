from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_week():
    current_week = datetime.now().isocalendar()[1]
    start_week = datetime.now().replace(month=9, day=1).isocalendar()[1]
    week = current_week - start_week + 1
    return week


def get_days(req):
    
    src = req.text

    soup = BeautifulSoup(src, 'html.parser')
    days = soup.findAll('div', class_='card')

    days_list = {'days': {}}
    for day in days:
        day_info = {'day_name': day.a.string.strip(), 'items': {}}
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
            print(day_info)
            print(item_info)
            
            day_info['items'].update(item_info)
        print(days_list)
        days_list['days'].update(day_info)
    print(days_list)
    return days_list



def parse(group, addgroup, week):
    req = requests.get(f'https://eners.kgeu.ru/apish2.php?group={group}&week={week}&type=one')
    addreq = requests.get(f'https://eners.kgeu.ru/apish2.php?group={addgroup}&week={week}&type=one')
    
    context = get_days(req)
    print(context)
    context['days']['items'].update(get_days(addreq)['days']['items'])
    return context
    

def index(request):
    context = {}
    return render(request, 'info/index.html', context)


def table(request):

    # st_accept = 'text/html'
    # st_useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'

    # headers = {
    # "Accept": st_accept,
    # "User-Agent": st_useragent
    # }

    week = get_week()

    group = 'ПИ-1-21'
    addgroup = 'ЦК-ДО-5'

    context = {}
    
    context.update(parse(group, addgroup, week))
    # req = requests.get(f'https://eners.kgeu.ru/apish2.php?group=ПИ-1-21&week={week}&type=one', headers)
    print(context)
    return render(request, 'info/table.html', context)