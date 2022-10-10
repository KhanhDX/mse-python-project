import urllib.request
from bs4 import BeautifulSoup

def crawlData():
    lst = []
    url = "http://127.0.0.1:5000/"
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('td')
    for i in range(0, len(tags), 8):
        data = ''
        data = data + 'RollNumber:' + tags[i].text + '\n'
        data = data + 'First Name:' + tags[i].text + '\n'
        data = data + 'Last Name:' + tags[i].text + '\n'
        data = data + 'Email:' + tags[i].text + '\n'
        data = data + 'Date of birth:' + tags[i].text + '\n'
        data = data + 'Address:' + tags[i].text + '\n'
        data = data + 'Score:' + tags[i].text + '\n'
        lst.append(data)
    with open('dataCrawl.txt', 'w', encoding='utf-8') as file:
        for i in range(0, len(lst)):
            s = 'Thong tin sinh vien thu: '
            s = s + str(i + 1) + '\n'
            file.write(s)
            file.write(lst[i])
            file.write("\n")

crawlData()