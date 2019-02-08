from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import sys
import paramiko
import time
import pyclamd
from concurrent.futures import ThreadPoolExecutor,wait
from threading import Thread
from django.views.decorators.csrf import csrf_protect



# Create your views here.




#设置系统用户名和名密码
@csrf_protect
@login_required(login_url='/login')
def useradd(request):
    if request.method == 'POST':
        hostname = request.POST['IP']
        username = request.POST['user']
        password = request.POST['passwd']
        useradd = request.POST['newuser']
        passwdadd1 = request.POST['newpasswd1']
        passwdadd2 = request.POST['newpasswd2']

        request.session['hostname'] = hostname
        request.session['username'] = username
        request.session['passworld'] = password
        request.session['useradd'] = useradd

        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname,username=username,password=password,timeout=10)
            t = True
        except Exception:
            t = False
            print('系统无法登陆')
            e = '系统无法链接'
            cantent = {'e': e}
            return render(request, 'security/useradd.html', cantent)
        if t:
            if passwdadd1 == passwdadd2:
                cmd = 'useradd '+useradd+'; echo '+passwdadd1+' | '+'passwd --stdin '+useradd
                stdin1, stdout1, stderr1 = ssh.exec_command(cmd)
                stdin = stdin1.read()
                stdout = stdout1.read()
                stderr = stderr1.read()
                cantent = {'stdin': stdin, 'stdont': stdout, 'stderr': stderr}
                request.session['cantent'] = cantent
                return render(request,'security/groupadd.html',cantent)
            else:
                u = '俩次输入的密码不对,请重新输入'
                cantent = {'u':u}
                return render(request,'security/useradd.html',cantent)
    else:
        return render(request,'security/useradd.html')




#将刚刚创建的用户添加到用户组
@csrf_protect
@login_required(login_url='/login')
def groupadd(request):
    content = request.session.get('content')
    if request.method == 'POST':
        hostname = request.session.get('hostname')
        username = request.session.get('username')
        password = request.session.get('password')
        useradd = request.session.get('useradd')
        groupname = request.POST['groupname']

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, username=username, password=password, timeout=10)
        except Exception:
            e = '无法链接服务器'
            content = {'e':e}
            return render(request, 'security/groupadd.html', content)
        cmd = 'gpasswd -a '+ useradd + groupname
        stdin1, stdout1, stderr1 = ssh.exec_command(cmd)
        stdin2 = stdin1.read()
        stdout2 = stdout1.read()
        stderr2 = stderr1.read()
        content = {'stdin2':stdin2,'stdou2':stdout2,'stderr2':stderr2}
        return render(request,'security/groupadd.html',content)
    return render(request, 'security/groupadd.html', content)





#用户手动将用户添加到指定的用户组中
@csrf_protect
@login_required(login_url='/login')
def usertogroup(request):
    if request.method == 'POST':
        hostname = request.POST['IP']
        username = request.POST['user']
        password = request.POST['passwd']
        adduser = request.POST['adduser']
        addgroup = request.POST['addgroup']

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, username=username, password=password, timeout=10)
        except Exception:
            e = '无法链接服务器'
            cantent = {'e': e}
            return render(request, 'security/usertogroup.html', cantent)

        cmd = 'usermod -a -G '+ adduser + addgroup
        stdin1, stdout1, stderr1 = ssh.exec_command(cmd)
        stdin = stdin1.read()
        stdout = stdout1.read()
        stderr = stderr1.read()
        content = {'stdin':stdin,'stdou':stdout,'stderr':stderr}
        return render(request,'security/usertogroup.html',content)
    return render(request, 'security/usertogroup.html')




#为服务器上的特殊文件设置特殊权限
@csrf_protect
def permission(request):
    if request.method == 'POST':
        IP = request.POST['IP']
        user = request.POST['user']
        passwd = request.POST['passwd']
        file = request.POST['file']
        radio =  request.POST.get('optionsRadios')
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=IP, username=user, password=passwd, timeout=10)
        except Exception:
            e = '无法链接服务器'
            content = {'e': e}
            return render(request, 'security/permission.html',content)
        cmd = 'chattr + ' + radio + " " + file
        stdin1, stdout1, stderr1 = ssh.exec_command(cmd)
        stdin = stdin1.read()
        stdout = stdout1.read()
        stderr = stderr1.read()
        contant = {'stdin':stdin,'stdou':stdout,'stderr':stderr}
        return render(request, 'security/permission.html',contant)
    return render(request,'security/permission.html')




#添加用户组
@csrf_protect
@login_required(login_url='/login')
def addgroup(request):
    if request.method == 'POST':
        hostname = request.POST['IP']
        username = request.POST['user']
        password = request.POST['passwd']
        newgroup = request.POST['newgroup']


        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname,username=username,password=password,timeout=10)
            t = True
        except Exception:
            t = False
            print('系统无法登陆')
            e = '系统无法链接'
            cantent = {'e': e}
            return render(request, 'security/addgroup.html', cantent)
        if t:
            cmd = 'groupadd '+ newgroup
            stdin1, stdout1, stderr1 = ssh.exec_command(cmd)
            stdin = stdin1.read()
            stdout = stdout1.read()
            stderr = stderr1.read()
            content = {'stdin':stdin, 'stdout':stdout, 'stderr':stderr}
            return render(request,'security/addgroup.html',content)
    return render(request,'security/addgroup.html')



#使用pyClamd经行病毒扫面
#在要扫面的服务器中安装clamavp相关程序包: clamav , clamd , clamav-update
@csrf_protect
@login_required(login_url='/login')
def virusscanning(request):
    class Scan(Thread):
        def __init__(self,IP,scan_type,file):
            Thread.__init__(self)
            self.IP = IP
            self.scan_type = scan_type
            self.connstr = ""
            self.scanresult = ""
        def run(self):
            try:
                cd = pyclamd.ClamdNetworkSocket(self.IP,3310)
                if cd.ping():
                    self.connstr = self.IP + "connection[OK]"
                    cd.reload()
                    if self.scan_type == "contscan_file":
                        self.scanresult = "{0}\n".format(cd.contscan_file(self.file))
                    elif self.scan_type == "multiscan_file":
                        self.scanresult = "{0}\n".format(cd.multiscan_file(self.file))
                    elif self.scan_type == "scan_file":
                        self.scanresult = "{0}\n".format(cd.scan_file(self.file))
                    time.sleep(2)
                else:
                    self.connstr = self.IP + "ping error,exit"
                    #contant = {'connstr':self.connstr}
                    #return  render(request,'security/virusscanning.html',contant)
            except Exception as e:
                self.connstr = self.IP + " " + str(e)
                #contant = {'connstr':self.connstr}
                #return render(request,'security/virusscanning.html',contant)


    if request.method == 'POST':
        IPs = request.POST['IPs']
        path = request.POST['path']
        radio = request.POST.get('optionsRadios')

        IPS = IPs.split(',')
        def conn():
            scanlist = []  # 存储扫描scan类线程对象列表
            i = 1
            for ip in IPS:
                currp = Scan(ip,radio,path)
                scanlist.append(currp)
                for task in scanlist:
                    task.start()
                for task in scanlist:
                    task.join()
                    connstr = task.connstr
                    scanresult = task.scanresult
                    yield connstr,scanresult

        con = conn()
        lis = list(con)
        contant = {'lis':lis}
        return render(request,'security/virusscanning.html',contant)

    return render(request,'security/virusscanning.html')




