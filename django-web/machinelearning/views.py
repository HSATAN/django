#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
from machinelearning.mongodb import db
from machinelearning.models import TOPIC
from machinelearning.forms import MODELORM,FILEFORM,PictureForm
import subprocess
import  socket
import logging
import json
# Create your views here.
def uppic(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        image = request.FILES.get('image')
        name=image.name
        cishi=name.count('.')
        if cishi>1:
            name=name.replace('.','',1)
        if form.is_valid():
            form.save()
            # return render(request,'machinelearning/index.html')/home/upload/picture
            form = PictureForm()
            context = {'form': form}
            return render(request, 'machinelearning/addpic.html', context=context)



        else:
            return HttpResponse('上传失败')

    else:
        form = PictureForm()
        context = {'form': form}
        return render(request, 'machinelearning/addpic.html', context=context)
def upload(request):
    '''
    文件上传方式1，用django的modelform生成表单，用django的框架处理保存上传的文件
    不需要自己读写文件，可以自己判断文件已存在时怎么处理
    :param request:
    :return:
    '''
    logger=logging.getLogger()
    if request.method=='POST':
        logger.warning("POST请求")
        form=FILEFORM(request.POST,request.FILES)
        if form.is_valid():
            logger.warning("数据合法")
            form.save()
            logger.warning("保存成功")
            logger.warning('执行到此')
            #return render(request,'machinelearning/index.html')
            return HttpResponse("上传成功")
        else:

           return HttpResponse('上传失败')

    else:
        logger.warning("GET请求")
        form=FILEFORM()
        context={'form':form}
        return render(request,'machinelearning/upload.html',context=context)
    pass
def upload1(request):
    '''
    文件上传方式2，用一般的request处理上传文件，需要自己读写文件
    需要自己添加判断文件是否存在，如果文件存在，处理文件的方式决定于你打开文件的方式，与一般的文件处理方式一样
    :param request:
    :return:
    '''
    if request.method=="POST":
        file = request.FILES.get('uploadfile')
        name = file.name#获取上传文件名，包括文件后缀
        path='machinelearning/static/'+name
        with open(path,'wb+') as f:
            f.write(file.read())
        return HttpResponse(path+"上传成功\nctest"+file.read().decode("utf-8"))
    else:
        return render(request,'machinelearning/upload1.html')


def topic(request,topic_id):
    '''显示id为topic_id的model'''
    logger=logging.getLogger()

    topic=TOPIC.objects.get(id=topic_id)
    context={'topic':topic}
    logger.warning("在topic中执行"+str(context))
    return render(request,'machinelearning/topic.html',context=context)
    pass

def topics(request):
    logger=logging.getLogger()

    logger.warning("在topics中执行")
    topics=TOPIC.objects.order_by('date_added')
    context={'topics':topics}
    return render(request, 'machinelearning/topics.html', context)
def new_topic(request):
    '''
    生成新的主题
    :param request:
    :return:
    '''
    if request.method !='POST':

        form = MODELORM()
        context= {'form':form}

        logger = logging.getLogger()

        logger.warning("在new_topic--if中执行"+str(context))
        return render(request,'machinelearning/new_topic.html',context)
    else:
        logger = logging.getLogger()
        form=MODELORM(request.POST, request.FILES)

        if form.is_valid():
            form.save()


            logger.warning("在new_topic +++--else中执行")
            return  HttpResponse('test')
        else:
            logger.warning("发生错误")
            #return HttpResponse("数据有错误")
    pass
def index(request):
    ip = request.META['REMOTE_ADDR']
    dir = os.listdir('machinelearning/static/pic')
    content = {'ip': ip, 'pic': dir}
    mongoclient=db.Mongo.get_mongo()
    mongo_db=mongoclient.visitor
    table=mongo_db.userip
    table.save({'_id':ip})
    mongoclient.close()
    return render(request, 'machinelearning/index.html',content)
#@login_required
def service(request):

    return render(request,'machinelearning/service.html')
    pass
def login(request):
    return  render(request,'machinelearning/login.html')

def handleCommand(request):
    '''获取表单数据的两种方法，一种事request.POST或者request.GET
    另一种是用django.forms模块生成clean_data
    '''
    command=request.POST.get('command')
    #result=os.system(command)#执行系统命令，不返回执行结果，只返回执行状态数字
    result=os.popen(command)#返回执行结果，调用read函数读取，如result.read()返回的事字符串
    '''这两个都是用当前进程来调用，也就是说它们都是阻塞式的。
    这两种执行系统命令的方式都是在当前进程中，命令执行完毕才会继续往下执行'''
    sub=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)


    return HttpResponse(socket.gethostbyname(socket.gethostname()))#request.POST获取表单传来的数据字典，用get函数取得名为command的值
    pass
def command(request):
    if request.method=='GET':
        return render(request,'machinelearning/command.html')
    else:

        return render(request,'machinelearning/command.html',context={'command':request.POST['command']})

def sync_info(responese):
    data={'original':{'test':'黄凯杰'}}
    #print(responese.POST['test'])
    print("kai")
    print(responese.method)

    return HttpResponse(responese.body)#response.body获取json数据
    pass