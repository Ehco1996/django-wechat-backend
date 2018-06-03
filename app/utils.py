import random
from base64 import b64decode

import requests
from bs4 import BeautifulSoup

from app import constants


def upload_to_sms(img_content):
    '''
    上传图片到smms
    数据返回格式请看文档 https://sm.ms/doc/
    '''
    post_data = {'smfile': b64decode(img_content)}
    r = requests.post(constants.SMS_API, files=post_data)
    return r.json()


def get_invite_code():
    r = requests.post('api_url', data={'token': 'token'})
    return r.json().get('msg')


def get_html_text(url):
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'something wrong'


def get_joke():
    '''
    抓取一个糗事段子
    '''

    html = get_html_text(
        'https://www.qiushibaike.com/8hr/page/{}/'.format(random.randint(1, 9)))
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all(
        'div', class_='article block untagged mb15 typs_hot')
    article = random.choice(articles)

    body = article.find('span').text
    author = article.find('img')['alt']
    try:
        comment = article.find(
            'div', class_='main-text').contents[0].replace('\n', '')
    except:
        comment = '暂时没有热评'

    joke = '作者：{}{}热评: {}'.format(author, body, comment)

    return joke
