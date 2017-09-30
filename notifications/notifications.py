#coding:utf-8

import sys
import os
import time
from threading import Thread
from models import *
from Channel import *

API_KEY_IOS = u"ymKdxPquXLurXqjfKbOT5hGL"
SECRET_KEY_IOS = u"0gf2WG4PUwmX8H3Sn8Yd7O8IXKxcSd1H"

API_KEY_ANDROID = u"az2xsngwymeWkKXgrR6CpdGM"
SECRET_KEY_ANDROID = u"6FloCZ6FrfzXrnaVmGMrAqL3V962qZUs"

DISNEY_TYPE = 'disney'
CONCERT_TYPE = 'concert'
AEROSPACE_TYPE = 'aerospace'
EXPLORE_TYPE = 'explore'
AGENT_TYPE = 'agent'
MOMENTS_TYPE = 'moments'

COMMENT_TYPE = 'Comment'
REGISTER_TYPE = 'Register'
LIKE_TYPE = 'Like'
DISLIKE_TYPE = 'Dislike'
APPROVED_TYPE = 'Approved'
DISAPPROVED_TYPE = 'Disapproved'
FAVORITE_TYPE = 'Favorite'
UNFAVORITE_TYPE = 'Unfavorite'

opts_android = {'msg_type':1, 'expires':300}
opts_ios = {'msg_type':1, 'expires':300, 'deploy_status':1}

def _get_device_params(user):
	try:
		user.usernotifications
	except:
		user_notifications = UserNotifications(user=user)
		user_notifications.save()
	if user.usernotifications is not None:
		user_id_baidu = user.usernotifications.user_id_baidu
		channel_id = user.usernotifications.channel_id
		device_type = user.usernotifications.device_type
		return {
			"user_id_baidu": user_id_baidu,
			"channel_id": channel_id,
			"device_type": device_type,
		}
	else:
		return False

def _push_post(recipient,trigger_user,post_text,*args,**kwargs):
    print args
    msg = "我发表了文章{0}.post_text".format(post_text.title)
    print msg
    new_notification = Notification()
    new_notification.trigger_user = trigger_user
    new_notification.banner = post_text.corresponding_post.banner
    new_notification.content = post_text.content
    new_notification.receive_user = recipient
    new_notification.content_id = post_text.corresponding_post.pk
    new_notification.content_type = MOMENTS_TYPE
    new_notification.save()

    device_info = _get_device_params(recipient)
    if not device_info:
        return False
    notifications = Notification.objects.filter(receive_user=recipient)
    badge = notifications.filter(is_read=False).count()
    return push_message(message = msg, badge = badge, **device_info)

def _push_comment(recipient,trigger_user,post_text,*args,**kwargs):
    msg = "{somebody}评论了文章{text}".format(somebody = trigger_user,text=post_text.title)
    print msg
    new_notification = Notification()
    new_notification.trigger_user = trigger_user
    new_notification.banner = post_text.corresponding_post.banner
    new_notification.content = post_text.content
    new_notification.receive_user = recipient
    new_notification.content_id = post_text.corresponding_post.pk
    new_notification.content_type = MOMENTS_TYPE
    new_notification.save()

    device_info = _get_device_params(recipient)
    if not device_info:
        return False
    notifications = Notification.objects.filter(receive_user=recipient)
    badge = notifications.filter(is_read=False).count()
    return push_message(message=msg, badge=badge, **device_info)

def push_message(user_id_baidu, channel_id, device_type, message, badge):
    # TODO: get the number of unread messages
    api_key = None
    secret_key = None
    message_params = {}

    if device_type == u'3': #Android
        api_key = API_KEY_ANDROID
        secret_key = SECRET_KEY_ANDROID
        message_params = {
			"title": "来自 尊享VIP 的消息",
			"description": message
		}
    if device_type == u'4': #iOS
        api_key = API_KEY_IOS
        secret_key = SECRET_KEY_IOS
        message_params = {
			"aps": {
				"content-available": 1,
				"badge": badge,
				"sound": "",
				"alert": message
			}
		}
    optional = {
		Channel.USER_ID: user_id_baidu,
		Channel.CHANNEL_ID: channel_id,
		Channel.PUSH_TYPE: 1,  #
		Channel.MESSAGE_TYPE: 1,  # 0: penetration 1: notification
		Channel.DEPLOY_STATUS: 1,  # production or development
	}
    channel = Channel(api_key, secret_key)
    try:
        ret = channel.pushMessage(1, json.dumps(message_params), 'key1', optional)
        print ret
        return True
    except KeyError, k:
        print '\nbaidu_push error No. is', str(k)
        return False

dispatcher = {
	"Comment": _push_comment,
	"Post":_push_post
    }

def async(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        # time.sleep(delay)
        t.start()

@async
def baidu_push(recipient, action, params, *args, **kwargs):
    print 1111
    dispatcher[action](recipient, **params)

