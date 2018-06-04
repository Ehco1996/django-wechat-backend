import time
import random
import base64
import hashlib
from urllib import parse
from collections import OrderedDict

import requests
from bosonnlp import BosonNLP

from app import constants

nlp = BosonNLP(constants.BOLSON_TOKEN)


def get_random_str():
    seeds = 'qwertyuiopasdfghjklzxcvbnm'
    return ''.join(random.choices(seeds, k=random.randint(1, 32)))


def get_req_sign(query_dict):
    keys = sorted(query_dict.keys())
    query = OrderedDict()
    for key in keys:
        query[key] = query_dict[key]
    query['app_key'] = constants.APP_KEY
    encode_str = parse.urlencode(query)
    md5 = hashlib.md5(encode_str.encode('utf-8'))
    return md5.hexdigest().upper()


def get_face_age(image_url):
    img = requests.get(image_url).content
    b64_img = base64.b64encode(img).decode('utf-8')
    img_size = len(b64_img) / 1000
    print('img size:', img_size)
    if img_size > 500:
        return {'ret': -1}
    query = {
        'app_id': constants.APP_ID,
        'time_stamp': int(time.time()),
        'nonce_str': get_random_str(),
        'image': b64_img,
    }
    query['sign'] = get_req_sign(query)
    resp = requests.post(constants.FACE_AGE_API, data=query)
    return resp.json()


def get_text_polar(text):
    '''语义分析'''
    query = {
        'app_id': constants.APP_ID,
        'time_stamp': int(time.time()),
        'nonce_str': get_random_str(),
        'text': text,
    }
    query['sign'] = get_req_sign(query)
    resp = requests.post(constants.TEXT_POLAR_API, data=query)
    return resp.json()


def get_boson_text_polar(text):
    ret = nlp.sentiment(text)[0]
    if ret[0] > ret[1]:
        return '积极语义'
    else:
        return '消极语义'
