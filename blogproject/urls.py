"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from blog import views
from django.conf import settings
# from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup\/*$', views.sign_up, name='sign_up'),
	url(r'^login\/*$', views.sign_in, name='login'),
	url(r'^logout\/*$', views.sign_out, name='logout'),
    url(r'^post\/?$', views.publish_post, name='publish_post'),
    url(r'^posts\/?$', views.get_posts, name='get_posts'),
    url(r'^posts/(?P<id>\d+)\/?$', views.get_post, name='get_post'),
    url(r'^posts/(?P<id>\d+)/comment\/?$', views.comment_post, name='get_comment'),
    url(r'^posts/(?P<id>\d+)/comments\/?$', views.get_comments, name='get_comments'),
    url(r'^posts/(?P<id>\d+)/delete\/?$', views.delete_post, name='delete_post'),
    url(r'^feedback\/?$', views.feed_back, name='feed_back'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]

# urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))