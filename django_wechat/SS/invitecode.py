
from lazyspider import lazystore
from .config import EHCO_DB


def get_invite_code():
    s = lazystore.LazyMysql(EHCO_DB)
    res = s.find_by_fields('shadowsocks_invitecode', {
        'code_id': 1, 'isused': 0})
    if res != -1:
        if len(res) > 0:
            return res[0]['code']
        else:
            return '邀请码用光啦'


