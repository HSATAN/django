# -*- coding:utf-8 -*-
from  django import forms
from .models import TOPIC,FILEMODEL,ImageModel

class MODELORM(forms.ModelForm):
    class Meta:
        model=TOPIC
        fields=['text','text1']#text为在FILE中的字段名，fields为要在form中显示的字段
        labels={'text':'请输入要添加的model','text1':'元数据'}#设置字段的label
        widgets={'text':forms.Textarea(attrs={'cols':20})}#设置字段的的输入框

class FILEFORM(forms.ModelForm):
    class Meta:
        model=FILEMODEL
        fields=['title','file']
class PictureForm(forms.ModelForm):
    class Meta:
        model=ImageModel
        fields=['image']