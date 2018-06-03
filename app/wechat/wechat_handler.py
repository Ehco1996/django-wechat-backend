import time
import logging
from base64 import b64decode

from django.template.loader import render_to_string

from app import constants
from app.wechat import models as m
from app.aiqq_api import get_face_age
from app.utils import get_invite_code, get_joke

logger = logging.getLogger('default')


def main_handler(xml):
    # 找到传来的消息事件：
    # 如果普通用户发来短信，则event字段不会被捕捉
    event = xml.find('Event')
    event = event.text if event is not None else None
    # 找到此次传送的消息信息的类型和内容
    msg_type = xml.find('MsgType')
    msg_content = xml.find('Content')
    msg_type = msg_type.text if msg_type is not None else None
    msg_content = msg_content.text if msg_content is not None else None

    logger.info("msg_type: {} event: {} content:{}".format(
        msg_type, event, msg_content))

    # 判断是否是新关注的用户
    if event == 'subscribe':
        text = constants.SUBSCRIBE_TEXT
        return parse_text(xml, text)

    if msg_type == 'image':
        return parse_image(xml)
    elif msg_type == 'text':
        if msg_content == '邀请码':
            text = get_invite_code()
            return parse_text(xml, text)
        elif msg_content == '段子':
            text = get_joke()
            return parse_text(xml, text)
        else:
            text = m.ReplyRule.get_reply(msg_content)
            return parse_text(xml, text)
    else:
        return 'success'


def parse_text(xml, text):
    '''
    处理微信发来的文本数据
    返回处理过的xml
    '''
    # 反转发件人和收件人的消息
    fromUser = xml.find('ToUserName').text
    toUser = xml.find('FromUserName').text
    # event事件是没有有msg id 的
    message_id = xml.find('MsgId')
    message_id = message_id.text if message_id is not None else ''
    # 我们来构造需要返回的时间戳
    nowtime = str(int(time.time()))
    context = {
        'FromUserName': fromUser,
        'ToUserName': toUser,
        'Content': text,
        'time': nowtime,
        'id': message_id,
    }
    # 我们来构造需要返回的xml
    respose_xml = render_to_string('wechat/wx_text.xml', context=context)
    logger.debug(respose_xml)
    return respose_xml


def parse_image(xml):
    '''
    处理微信发来的图片数据
    '''
    # 反转发件人和收件人的消息
    fromUser = xml.find('ToUserName').text
    toUser = xml.find('FromUserName').text
    message_id = xml.find('MsgId').text
    media_id = xml.find('MediaId').text
    nowtime = str(int(time.time()))
    pic_url = xml.find('PicUrl').text
    user_img_count = m.UserPic.objects.all().count()
    img_name = "{}.png".format(user_img_count)

    # 请求ai.qq.com 识别照片的年龄和颜值
    resp = get_face_age(pic_url)
    if resp['ret'] != 0:
        text = resp['msg']
    else:
        img_data = b64decode(resp['data']['image'])
        text = m.UserPic.upload_img(toUser, media_id, img_name, img_data)
    context = {
        'FromUserName': fromUser,
        'ToUserName': toUser,
        'Content': text,
        'time': nowtime,
        'id': message_id,
    }
    # 我们来构造需要返回的xml
    respose_xml = render_to_string('wechat/wx_text.xml', context=context)
    logger.debug(respose_xml)
    return respose_xml
