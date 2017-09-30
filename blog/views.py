#-*- coding: utf-8 -*-
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.forms import *
import utils as utils
from notifications.notifications import *
from cms.models import Feedback

#注册系统
@require_POST
@csrf_exempt
def sign_up(request):
	form = UserForm(request.POST)
	if form.is_valid():
		# 获取表单信息
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		# 将表单写入数据库
		filterResult = User.objects.filter(username=username)
		if len(filterResult) > 0:
			return HttpResponseBadRequest('用户已存在')
		User.objects.create_user(username=username, email=email, password=password)
		user = authenticate(username=username, password=password)
		if user.is_active:
			login(request, user)
		else:
			return HttpResponseBadRequest('账户未激活')
		return HttpResponse("注册成功")
	return HttpResponseBadRequest('注册失败')

#登录系统
@require_POST
@csrf_exempt
def sign_in(request):
	try:
		name = request.POST['name']
		code = request.POST['code']
	except:
		return HttpResponseBadRequest('参数不正确')

	user = authenticate(username=name, password=code)
	print user
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponse("登录成功")
		else:
			return HttpResponseBadRequest("账户未激活")
	else:
		return HttpResponseBadRequest("账号不存在/验证码错误, 登录失败")

@login_required
@require_GET
def sign_out(request):
	logout(request)
	return HttpResponse("注销成功")

#发布博客
@csrf_exempt
@require_POST
@login_required
def publish_post(request):
	user = request.user
	text = request.POST.get('text')
	title = request.POST.get('title')
	files = request.FILES
	if text is None or not len(text):
		return HttpResponseBadRequest("请填写正确参数")
	print "ture",utils.contains_sensitive(text)
	if utils.contains_sensitive(text):
		return HttpResponseBadRequest('博客正文违反相关法律法规请重新输入!')

	try:
		new_post = Post()
		new_post.text = text
		new_post.title = title
		new_post.author = user
		if 'picture' in files:
			form = ImageUploadForm(request.POST, files)
			if not form.is_valid():
				return HttpResponseBadRequest("上传图片损坏或格式错误, 添加失败")
			new_post.picture = form.cleaned_data['picture']
		if 'video' in files:
			form = DocumentForm(request.POST,files)
			if not form.is_valid():
				return HttpResponseBadRequest("上传视频损坏或格式错误, 添加失败")
			new_post.video = form.cleaned_data['videl']
		new_post.save()

	except ValueError:
		return HttpResponseBadRequest("参数传值有错,发表博客失败")
	# baidu_push(recipient=user, action="Post", params={
	# 	'post_text': new_post,
	# 	'trigger_user': request.user
	# })
	return HttpResponse("发表博客成功")


# def upload_pic(request):
# 	if request.method == 'POST':
# 		form = ImageUploadForm(request.POST, request.FILES)  # 有文件上传要传如两个字段
# 		if form.is_valid():
# 			m = ExampleModel.objects.get(pk=course_id)
# 			m.model_pic = form.cleaned_data['image']  # 直接在这里使用 字段名获取即可
# 			m.save()
# 			return HttpResponse('image upload success')
# 	return HttpResponseForbidden('allowed only via POST')





#获取博客列表
@require_GET
def get_posts(request):
	# current_user = request.user
	posts = Post.objects.all().order_by('-publish_time')
	json_list = []

	for post in posts:
		post_detail = post.to_json()
		json_list.append(post_detail)
	return JsonResponse(json_list, safe=False)

#获取博客详情
@require_GET
def get_post(request, id):
	try:
		model_post = Post.objects.get(pk =id)
		post_detail = model_post.to_json()
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到博客{0}".format(id))
	return JsonResponse(post_detail, safe = False)

#评论博客
@csrf_exempt
@require_POST
@login_required
def comment_post(request, id):
	comment = request.POST.get('text')
	if comment is None:
		return HttpResponseBadRequest("请填写正确评论")
	# if len(comment) > MomentsComments._meta.get_field('content').max_length:
	# 	return HttpResponseBadRequest('圈子评论长度超过限制')
	try:
		post = Post.objects.get(pk=id)
		user = request.user
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到对应博客")
	try:
		new_comment = PostComments()
		new_comment.content = comment
		new_comment.corresponding_post = post
		new_comment.corresponding_user = user
		new_comment.save()
		baidu_push(recipient=user, action='Comment', params={
			'post_text': new_comment,
			'trigger_user': request.user
		})
		return HttpResponse("评论成功")
	except ValueError:
		return HttpResponseBadRequest("评论参数传值有错,提交评论失败")

#获取评论
@require_GET
def get_comments(request, id):
	comments = PostComments.objects.filter(corresponding_post_id = id).order_by('-publish_time')
	json_list = []
	for comment in comments:
		comment_detail = comment.to_json()
		json_list.append(comment_detail)
	return JsonResponse(json_list, safe = False)

#删除博客
@require_GET
@login_required
def delete_post(request, id):
	try:
		post = Post.objects.get(pk=id)
		current_user = request.user
		if post in Post.objects.filter(author=current_user):
			post.delete()
		else:
			return HttpResponseForbidden("博客不是当前登录用户所发布, 不能删除")
	except ObjectDoesNotExist:
		return HttpResponseNotFound("找不到博客{0}".format(id))
	return HttpResponse("删除博客{0}成功".format(id))

#意见反馈
@require_POST
@login_required
@csrf_exempt
def feed_back(request):
	text = request.POST.get('text')

	if text is None:
		return HttpResponseBadRequest("意见填写为空,请重新填写")
	if utils.contains_sensitive(text):
		return HttpResponseBadRequest("意见不符合相关规定,请重新输入")
	if len(text) > Feedback._meta.get_field('text').max_length:
		return HttpResponseBadRequest("意见长度超过限制")
	try:
		new_feedback = Feedback()
		new_feedback.text = text
		new_feedback.save()

	except ValueError:
		return HttpResponseBadRequest("意见反馈参数传值有错")
	return HttpResponse("反馈成功 ")




