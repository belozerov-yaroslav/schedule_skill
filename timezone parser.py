import csv

from requests import get
from bs4 import BeautifulSoup


def parse():
    timezones = []
    with open('timezones.html') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.find_all('tr'):
        time_list = []
        for q in i.find_all('td'):
            time_list.append(q.get_text())
        timezones.append(time_list)
    with open('times.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f, delimiter=';')
        for i in timezones:
            writer.writerow([q.strip() for q in i])


inf = {}
with open('times.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=';')
    for i in reader:
        if i:
            inf[i[2]] = int(i[5][1:3].replace('в€’', '-')) * 1 if i[5][0] == '+' else -1
print(inf)
print(inf['Europe/Moscow'])
