from bs4 import BeautifulSoup
import urllib.request, urllib.parse


def crawling_cine():
    list_record=[]

    for i in range(1,3): # 10페이지까지 하고싶으면 11로 
        params = urllib.parse.urlencode({'page':i})
        url = 'https://movie.naver.com/movie/point/af/list.nhn?&%s' %params
        req = urllib.request.urlopen(url)
        navigator = BeautifulSoup(req,'html.parser')
        table = navigator.find('table', class_='list_netizen')

        for i,r in enumerate(table.find_all('tr')):
            for j,c in enumerate(r.find_all('td')):
                if j==0:
                    record = {'num':int(c.text.strip())}
                elif j==2:
                    record.update({'score':int(c.text.strip())})
                elif j==3:
                    record.update({'title':str(c.find('a',class_='movie').text.strip())})
                    record.update({'opinion':str(c.text).split('\n')[2]})
                elif j==4:
                    record.update({'author':c.find('a',class_='author').text.strip()})
                    record.update({'date':str(c.text).split('****')[1]})
            try:
                list_record.append(record)
            except:
                pass
    
    return list_record





