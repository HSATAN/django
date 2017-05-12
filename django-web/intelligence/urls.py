# -*- coding:utf-8 -*-
"""intelligence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from machinelearning.views import index,service,login,command,handleCommand,topics,new_topic,topic,upload,upload1,sync_info
from machinelearning.views import uppic,learn,addTopic,showTopic,picture
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',index),
    url(r'^service/',service),
    url(r'^command/',command),
    url(r'^accounts/login/',login),
    url(r'^handleCommand/',handleCommand),
    url(r'^topics/$',topics),
    url(r'^new_topic/',new_topic),
    url(r'^topics/(?P<topic_id>\d+)/$',topic),
    url(r'^upload/$',upload),
    url(r'^upload1/$',upload1),
    url(r'^sync_info/$',sync_info),
    url(r'^uppic/$',uppic),
    url(r'^learn/$',learn),
    url(r'^addtopic/$',addTopic),
    url(r'^topic/',showTopic),
    url(r'^picture$',picture)
]
