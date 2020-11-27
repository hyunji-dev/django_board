"""pyboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from board import views
from board.views import reply_insert


urlpatterns = [
    path('admin/', admin.site.urls), # 관리자용 사이트 
    
    path('', views.main),
    
    # 요청 리퀘스트 적어주면 됨 
    # 게시판 관련 url 
    path('list/', views.list), 
    path('write', views.write),
    path('insert', views.insert),
    path('download', views.download),
    path('detail', views.detail),
    path('update', views.update),
    path('delete', views.delete),
    path('reply_insert', views.reply_insert),
    
    # 영화 리뷰, 평점 웹크롤링 관련 url 
    path('movie_save', views.movie_save),
    
    # 차트 
    path('chart', views.chart),
    
    # 워드클라우드
    path('wordcloud', views.wordcloud),
    
    # 위치 지도 
    path('map', views.cctv_map),
    
    
]
