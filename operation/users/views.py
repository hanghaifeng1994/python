from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from .forms import CustonForm,ModileInformationForm
from .models import CommonerUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect


# Create your views here.




#主页
@csrf_protect
def home(request):
    return render(request,'users/home.html')


'''
创建超级用户：
        python manage.py createsuperuser
        
        用户名：admin
        密码：harry1994
'''
#登陆
@csrf_protect
def loginone(request):
    if request.method == 'POST':
        user = authenticate(request,username=request.POST['username'],password=request.POST['password']) #判断用户是否存在
        if user is None: #用户不存在，返回None
            return render(request,'users/login.html',{'error':'用户不存在或密码不对'})
        else:
            login(request,user) #让用户登陆进去
            return redirect('/app_bar')
    else:
        return render(request,'users/login.html')



#登出
@csrf_protect
def logoutone(request):
    logout(request)
    return render(request,'users/login.html')



#注册
@csrf_protect
def registerone(request):
    if request.method == 'POST':
        form = CustonForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            CommonerUser(user=user,nickname=form.cleaned_data['nickname'],birthday=form.cleaned_data['birthday']).save()
            login(request,user)
            return redirect('/')
    else:
        form = CustonForm()
    content = {'form':form}
    return render(request,'users/register.html',content)



#个人中心
@csrf_protect
@login_required(login_url='/login')
def userCenter(request):
    content = {'user':request.user}
    return render(request,'users/user_center.html',content)



#编辑个人信息
@csrf_protect
@login_required(login_url='/login')
def editProfile(request):
    if request.method == 'POST':
        editForm = ModileInformationForm(request.POST,instance=request.user)
        if editForm.is_valid():
            editForm.save()
            request.user.CommonerUser.nickname = editForm.cleaned_data['nickname']
            request.user.CommonerUser.birthday = editForm.cleaned_data['birthday']
            request.user.CommonerUser.save()
            return redirect('/user_center')
    else:
        editForm = ModileInformationForm(instance=request.user)
    content = {'editForm':editForm,'user':request.user}
    return render(request,'users/edit_profile.html',content)



#修改密码
@csrf_protect
@login_required(login_url='/login')
def changePassword(request):
    if request.method == 'POST':
        change = PasswordChangeForm(data=request.POST,user=request.user)
        if change.is_valid():
            change.save()
            return redirect('/login')
    else:
        change = PasswordChangeForm(user=request.user)
    content = {'change':change,'user':request.user}
    return render(request,'users/change_password.html',content)



#导航栏
@csrf_protect
def appBar(request):
    return render(request,'users/app_bar.html')