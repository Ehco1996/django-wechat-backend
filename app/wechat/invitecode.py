import requests

URL = ''
TOKEN = ''


def get_invite_code():
    r = requests.post(URL, data={'token': TOKEN})
    return r.json().get('msg')


#res = get_invite_code()
# print(res)
