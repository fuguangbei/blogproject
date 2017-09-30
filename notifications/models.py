#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import blog.utils as utils
from django.contrib.auth.models import User


def post_banner_upload_path(instance, filename):
	ext = utils.get_file_extension(filename)
	file_path = "banner.{ext}"
	return file_path.format(id=instance.pk, ext=ext)

# Create your models here.
@python_2_unicode_compatible
class Notification(models.Model):
    class Meta:
        verbose_name = "消息通知"
        verbose_name_plural = "消息通知"

    ACTION_CHOICES = (('Post', '发表了'), (' comment', '评论了'))
    TYPE_CHOICES = (
        ('moments', '博客'),
    )
    content_type = models.CharField(max_length = 10,choices = TYPE_CHOICES, default = '')
    content_id = models.IntegerField(verbose_name= "推送内容对应id", blank= True,default=0)
    action= models.CharField(max_length = 20,choices= ACTION_CHOICES, default='')
    time = models.DateTimeField(verbose_name= "通知时间",auto_now_add= True)
    content = models.CharField(
        max_length=200,
        verbose_name="内容",
        blank=True
    )
    triggering_user = models.ForeignKey(
        User,
        related_name="triggering_user",
        on_delete = models.CASCADE,
        verbose_name ="触发者"
    )
    receive_user = models.ForeignKey(
        User,
        related_name="receive_user",
        on_delete =models.CASCADE,
        verbose_name="接受者",
        null=True,
        blank = True
    )
    banner = models.ImageField(
        upload_to=post_banner_upload_path,
        verbose_name="消息封面缩略图",
    )
    is_read= models.BooleanField(
        verbose_name="是否已读",
        default=False
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.banner
            self.banner = None
            super(Notification, self).save(*args, **kwargs)
            self.banner = saved_image
        super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    def to_json(self):
        triggering_user_info = {
            'name': self.triggering_user.profile.get_nickname(),
            'avatar': self.triggering_user.profile.get_avatar()
        }
        this = {
            'id':self.pk,
            'push_content':{
                "text":self.content,
                "banner":self.banner.url if self.banner else "",
                'content_type':self.content_type,
                'content_id':self.content_id
            },
            'is_read':self.is_read,
            'action':self.get_action_display(),
            'triggering_user':triggering_user_info
        }
        return this

@python_2_unicode_compatible
class UserNotifications(models.Model):
    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = '用户消息'
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    DEVICE_CHOICE = (('3','Android'),('4','IOS'))
    device_type = models.CharField(max_length=1,choices = DEVICE_CHOICE,default='')
    user_id_baidu = models.CharField(max_length=25,default='',blank=True)
    channel_id = models.CharField(max_length=20,blank=True)

    def update_device_parm(self, channel_id, userid, device_type):
        self.channel_id =channel_id
        self.user_id_baidu = userid
        self.device_type = device_type
        self.save()

    def __str__(self):
        return self.user.username