"""qrmProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
# Report app URL Conf
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from .views import *
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'list'), # 메인 리스트 URL
    # 파일 업로드 후 Compare 하기 위한 Compare 버튼 클릭 시 호출되는 URL 정의
    # 다른 경로로 이동 되진 않고 Compare 로직 수행 후 메인페이지 재로드 함
    url(r'^(?P<pk>[0-9]+)$', views.compare, name = 'compare'),
    # 단어 사전 페이지(리스트, 추가, 수정, 삭제)
    url(r'^word/$', views.word_list, name = 'word_list'),
    url(r'^word/add/$', WordDictCreateView.as_view(), name = 'word_add'),
    url(r'^word/(?P<pk>[0-9]+)/$', WordDictUpdateView.as_view(), name = 'word_modify'),
    url(r'^word/(?P<pk>[0-9]+)/delete/$', WordDictDeleteView.as_view(), name = 'word_del'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # 정적 파일 및 업로드 한 파일을 서빙하기 위한 URL 패턴 정의
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)