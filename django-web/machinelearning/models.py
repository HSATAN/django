#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class TOPIC(models.Model):
    text=models.CharField(max_length=200)
    text1=models.CharField(max_length=100)
    #file=models.FileField(upload_to='files/')
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text

class FILEMODEL(models.Model):
    title=models.CharField(max_length=100)
    file=models.FileField(upload_to='upload/%Y%m%d')

    # upload保存文件的存储目录，和setting文件中的MEDIA_ROOT设置的目录组合在一起生成文件的保存路径
    def __str__(self):
        return  self.title
class ImageModel(models.Model):
    image=models.ImageField(upload_to='machinelearning/static/pic')

