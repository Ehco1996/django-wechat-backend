from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
from django.utils.encoding import smart_str
import hashlib
import time
from django.template.loader import render_to_string

from .ss_invite import code_back

# Create your views here.

# 公众号自定义的token
TOKEN = 'ehcotest2017'

# csrf_exempt 标记是为了取消django自带的csrf标记


def mirrorback(xml):
    '''
    处理微信发来的数据，
    这里仅仅返回用户发来的消息
    str 是微信服务器post来的xml格式的数据

    返回处理过的xml
    '''

    # 我们翻转发件人和收件人的消息
    fromUser = xml.find('ToUserName').text
    toUser = xml.find('FromUserName').text
    content = xml.find('Content').text
    message_id = xml.find('MsgId').text

    # 我们来构造需要返回的时间戳
    nowtime = str(int(time.time()))

    context = {
        'FromUserName': fromUser,
        'ToUserName': toUser,
        'Content': content,
        'time': nowtime,
        'id': message_id,
    }
    # 我们来构造需要返回的xml
    respose_xml = render_to_string('SS/wx_text.xml', context=context)

    return respose_xml


@csrf_exempt
def wechat(request):
    '''
    所有的消息都用进过这个函数进行验证处理
    微信验证的消息是以GET方式获得的
    平时的收发则以POST的方式
    '''

    if request.method == 'GET':
        # 我们来获取微信给我们发送的验证消息
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        token = TOKEN

        # 按照微信的验证要求将token字段timestamp、nonce字段惊醒字典顺序排序
        # 将三个参数字符串拼接成一个字符串进行sha1加密
        # 获得加密后的字符串可与signature对比，标识该请求来源于微信
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        hashstr = "%s%s%s" % tuple(tmp_list)
        hashstr = hashlib.sha1(hashstr.encode('utf-8')).hexdigest()

        # 如果得出的结果和微信服务器发来的相同，则将echostr返回去
        # 就能成功对接了
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('wx_index')

    if request.method == 'POST':
        # 从微信服务器获得转发来的各种消息

        # 这里将获取到的非uicode字符转换为可以处理的字符编码
        data = smart_str(request.body)
        xml = etree.fromstring(data)

        # 在控制台输出一下挑调试信息
        print(data)

        # 找到此次传送的消息信息
        msg_type = xml.find('MsgType').text
        content = xml.find('Content').text
        print(msg_type, content)

        # 将数据处理后发出
        if content == '邀请码':
            respose_xml = code_back(xml)
        else:
            respose_xml = mirrorback(xml)

        print(respose_xml)

        return HttpResponse(respose_xml)
