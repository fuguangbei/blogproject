#-*- coding: utf-8 -*-
from django import forms
from models import *

class UserForm(forms.Form):
	username = forms.CharField(label='用户名：',max_length=10)
	password = forms.CharField(label='密码：',widget=forms.PasswordInput())
	email = forms.EmailField(label='电子邮件：')

class ImageUploadForm(forms.Form):
	picture = forms.ImageField()

class DocumentForm(forms.Form):
	video = forms.FileField(label='视频')