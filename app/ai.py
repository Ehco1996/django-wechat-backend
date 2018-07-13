import time
import random
import base64
import hashlib
from urllib import parse
from collections import OrderedDict

import requests
from requests.adapters import Retry
from requests.adapters import HTTPAdapter


class TencentAiHandler:
    '''腾讯开放平台'''
    TTS_API = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tts'
    FACE_AGE_API = 'https://api.ai.qq.com/fcgi-bin/ptu/ptu_faceage'
    TEXT_POLAR_API = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar'

    def __init__(self, app_id, app_key):
        self.session = requests.Session()
        # add requests http adapter with retry, including
        http_adapter = HTTPAdapter(max_retries=Retry(
            total=3, method_whitelist=frozenset(['GET', 'POST', 'PUT'])))
        self.session.mount('https://', http_adapter)

        self.app_id = app_id
        self.app_key = app_key

    def _get_random_str(self):
        seeds = 'qwertyuiopasdfghjklzxcvbnm'
        return ''.join(random.choices(seeds, k=random.randint(1, 32)))

    def _get_req_sign(self, query_dict):
        keys = sorted(query_dict.keys())
        query = OrderedDict()
        for key in keys:
            query[key] = query_dict[key]
        query['app_key'] = self.app_key
        encode_str = parse.urlencode(query)
        md5 = hashlib.md5(encode_str.encode('utf-8'))
        return md5.hexdigest().upper()

    def get_tts_content(self, text):
        '''
        params:
            speaker : 普通话男声:1 静琪女声:5 欢馨女声:6 碧萱女声:7
            format  : PCM:1 WAV:2 MP3:3
            speed   : 50~200
        doc: https://ai.qq.com/doc/aaitts.shtml
        '''
        query = {
            'app_id': self.app_id,
            'time_stamp': int(time.time()),
            'nonce_str': self._get_random_str(),
            'speaker': 1,
            'format': 3,
            'volume': 0,
            'speed': 100,
            'text': text,
            'aht': 0,
            'apc': 58
        }
        query['sign'] = self._get_req_sign(query)
        res = self.session.post(
            TencentAiHandler.TTS_API, data=query).json()
        if res['ret'] != 0:
            print(res['msg'])
            return None
        else:
            b64_voice_content = res['data']['speech']
            content = base64.b64decode(b64_voice_content)
            return content

    def get_face_age(self, image_url):
        '''颜龄检测'''
        img = self.session.get(image_url).content
        b64_img = base64.b64encode(img).decode('utf-8')
        img_size = len(b64_img) / 1000
        print('img size:', img_size)
        if img_size > 500:
            return {'ret': -1}
        query = {
            'app_id': self.app_id,
            'time_stamp': int(time.time()),
            'nonce_str': self._get_random_str(),
            'image': b64_img,
        }
        query['sign'] = self._get_req_sign(query)
        resp = self.session.post(TencentAiHandler.FACE_AGE_API, data=query)
        return resp.json()


def get_text_polar(self, text):
    '''语义分析'''
    query = {
        'app_id': self.APP_ID,
        'time_stamp': int(time.time()),
        'nonce_str': self._get_random_str(),
        'text': text,
    }
    query['sign'] = self._get_req_sign(query)
    resp = self.session.post(TencentAiHandler.TEXT_POLAR_API, data=query)
    return resp.json()
