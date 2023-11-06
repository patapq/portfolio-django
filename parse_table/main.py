import requests
from bs4 import BeautifulSoup


st_accept = 'text/html'
st_useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'

headers = {
   "Accept": st_accept,
   "User-Agent": st_useragent
}


req = requests.get('https://eners.kgeu.ru/apish2.php?group=ПИ-1-21&week=11&type=one', headers)
src = req.text

soup = BeautifulSoup(src, 'html.parser')

days = soup.findAll('div', class_='card')

for day in days:
    print(day.a.string.strip())
    items = day.select('.list-group-item')
    for k, item in enumerate(items):
        time = '-'.join(item.select_one('.col-sm-2').text.strip().split(' '))
        subject = item.select_one('.col-sm-6').text.strip()
        cabinet = item.select_one('.col-sm-4 .tx-normal').text.strip()
        instructor = item.select_one('.col-sm-4 .text-muted').text.strip()

        print(k + 1, end=') ')
        print(time)
        print(subject)
        print(cabinet)
        print(instructor)
        print('-')
    print('--------------------')
   
