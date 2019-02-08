from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms



#自定义个人信息表单
class CustonForm(UserCreationForm):
    nickname = forms.CharField(required=False,max_length=50)
    birthday = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ('username','password1','password2','email','nickname','birthday')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].error_messages = {'unique':'用户名已存在！','invalid':'格式不对'}






#自定义修改个人信息表单
class  ModileInformationForm(UserChangeForm):
    nickname = forms.CharField(required=False,max_length=50)
    birthday = forms.DateField(required=False)

    class Meta:
        model = User
        fields = ('username','password','email','nickname','birthday')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].error_messages = {'unique':'用户名已存在！','invalid':'格式不对'}
