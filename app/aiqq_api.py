import time
import random
import base64
import hashlib
from urllib import parse
from collections import OrderedDict

import requests

from app.constants import APP_KEY, FACE_AGE_API, APP_ID


def get_random_str():
    seeds = 'qwertyuiopasdfghjklzxcvbnm'
    return ''.join(random.choices(seeds, k=random.randint(1, 32)))


def get_req_sign(query_dict):
    keys = sorted(query_dict.keys())
    query = OrderedDict()
    for key in keys:
        query[key] = query_dict[key]
    query['app_key'] = APP_KEY
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
        'app_id': APP_ID,
        'time_stamp': int(time.time()),
        'nonce_str': get_random_str(),
        'image': b64_img,
    }
    query['sign'] = get_req_sign(query)
    resp = requests.post(FACE_AGE_API, data=query)
    return resp.json()
