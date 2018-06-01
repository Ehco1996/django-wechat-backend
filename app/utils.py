from base64 import b64decode

import requests

from app.constants import SMS_API


def upload_to_sms(img_content):
    '''
    上传图片到smms
    数据返回格式请看文档 https://sm.ms/doc/
    '''
    post_data = {'smfile': b64decode(img_content)}
    r = requests.post(SMS_API, files=post_data)
    return r.json()
