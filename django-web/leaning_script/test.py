# -*- coding:utf-8 -*-
from lxml import etree
message='''<xml>
<ToUserName><![CDATA[你好]]></ToUserName>
<FromUserName><![CDATA[{1}]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{2}]]></Content>
</xml>'''
data=etree.fromstring(message)
ToUserName=data.find('ToUserName').text
FromUserName=data.find('FromUserName').text
CreateTime=data.find('CreateTime').text
Content=data.find('Content').text
print(ToUserName)
print(FromUserName)
print(CreateTime)
print(Content)