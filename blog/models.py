#-*- coding:utf-8*-*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import blog.utils as utils

def post_banner_upload_path(instance, filename):
	ext = utils.get_file_extension(filename)
	file_path = "picture{id}.{ext}"
	return file_path.format(id=instance.pk, ext=ext)

def post_video_upload_path(instance, filename):
	ext = utils.get_file_extension(filename)
	file_path = "video{id}.{ext}"
	return file_path.format(id=instance.pk, ext=ext)

@python_2_unicode_compatible
class Post(models.Model):
	class Meta:
		verbose_name = "博客"
		verbose_name_plural ="博客"

	title = models.CharField(verbose_name = "标题", max_length =20)
	author = models.ForeignKey(User, verbose_name ="作者", on_delete=models.CASCADE)
	publish_time = models.DateTimeField(verbose_name = "发布时间", auto_now_add = True)
	text = models.TextField(verbose_name='正文')
	picture = models.ImageField(
		upload_to= post_banner_upload_path,
		verbose_name="图片",
		null=True,
		blank = True
	)
	video = models.FileField(verbose_name = "视频", upload_to=post_video_upload_path, null=True, blank=True)

	def to_json(self):
		this ={
			'id':self.pk,
			'title':self.title,
			'text':self.text,
			'author':self.author.username,
			'picture':self.picture.url if self.picture else '',
			'video':self.video.url if self.video else ''
			}
		return this

	def __str__(self):
		return self.title

@python_2_unicode_compatible
class PostComments(models.Model):
	class Meta:
		verbose_name = '博客评论'
		verbose_name_plural = '博客评论'

	publish_time = models.DateTimeField(auto_now_add=True)
	content = models.CharField(max_length=140, verbose_name='评论')
	corresponding_post = models.ForeignKey(
		Post,
		related_name='post_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	corresponding_user = models.ForeignKey(
		User,
		related_name='post_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)

	def __str__(self):
		return self.content

	def to_json(self):
		this = {
			'id': self.pk,
			'user': self.corresponding_user.username,
			'date': self.publish_time,
			'text': self.content
		}
		return this
