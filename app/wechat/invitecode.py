import base64
import requests

USERNAME = ''
PORT = 1

URL = 'https://www.ehcozone.ml/api/get/invitecode/'
TOKEN = base64.b64encode(
    bytes('{}+{}'.format(USERNAME, PORT), 'utf8')).decode()


def get_invite_code():
    r = requests.post(URL, data={'token': TOKEN})
    return r.json().get('msg')


#res = get_invite_code()
# print(res)
