import requests
import random
import re
import json
from multiprocessing import Pool
from requests.exceptions import RequestException


def get_one_page(url,header,proxy):
    try:
        response=requests.get(url,headers=header,proxies=proxy,timeout=25)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return 'err'

def pase_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?title="(.*?)".*?</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items=re.findall(pattern,html)
    for i in items:
        yield {
            'index':i[0],
            'image':i[1],
            'title':i[2],
            'actor':i[3].strip()[3:],
            'time':i[4].strip()[5:],
            'score':i[5]+i[6]
        }

def write_to_file(content):
    with open('猫眼电影.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main(offset):
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    ]
    proxy_list = [
        '27.191.234.69:9999',
        '58.249.55.222:9797',
        '39.106.114.143:80',
        '58.222.32.77:8080',
        '39.106.66.178:80',
        '218.60.8.99:3129'
    ]
    #header={'User-Agent':'Mozilla%2F5.0+(X11%3B+Ubuntu%3B+Linux+x86_64%3B+rv%3A72.0)+Gecko%2F20100101+Firefox%2F72.0'}
    header=random.choice(my_headers)
    proxy={'http':random.choice(proxy_list)}
    url='https://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url,header,proxy)
    for i in pase_one_page(html):
        write_to_file(i)

if __name__=='__main__':
    offsets=3
    for offset in range(offsets):
        main(offset)






