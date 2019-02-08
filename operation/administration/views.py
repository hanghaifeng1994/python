from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

# Create your views here.



import paramiko
from django.views.generic import View
from .models import Cpu,Mem,Io,Net
from django.contrib.auth.decorators import login_required
import time
import psutil
import os
import requests
import json
import math
from io import StringIO
from django.core import serializers




from common.mymako import render_json
from celery import task
#用于查询指定服务器的CPU , 内存 ， 磁盘，网络信息
@task()
@csrf_protect
@login_required(login_url='/login')
def systeminfo(request):
        times = time.time()
        IP = request.POST['IP']
        username = request.POST['username']
        passwd = request.POST['passwd']

        #try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=IP, username=username, password=passwd)
        #except Exception:
                #e = '服务器无法连接'
                #contant = {'e':e}
                #return  render(request,'adminstration/inputinfo.html',contant)

        #检测CPU信息---------------------------------------------------------------------------------
        cmdCPU = "CPU=`python -c 'import psutil;psutil.cpu_time()'`;echo $CPU"
        cpustdin1,cpustdout1,cpustderr1 = ssh.exec_command(cmdCPU)
        cpustderr = cpustderr1.read()
        cpu = cpustdout1.read()
        cpuuser = cpu.user #获取用户的CPU时间比
        Cpu(user=cpuuser,times=times).save().save()

        #查看系统内存----------------------------------------------------------------------------------
        cmdMEM = "MEM=`python -c 'import psutil;psutil.virtual_memory()'`;echo $MEM"
        memstdin1, memstdout1, memstderr1 = ssh.exec_command(cmdMEM)
        mem = memstdout1.read()
        memtotal = mem.total #系统总计内存
        memused = mem.used #系统已经使用内存
        memfree = mem.free #系统空闲内存
        Mem(times=times,total=memtotal,used=memused,free=memfree).save()

        #获取硬盘总的IO个数--------------------------------------------------------------------------
        cmdIO = "IO=`python -c 'import psutil;psutil.disk_io_counters()'`;echo $IO"
        iostdin1, iostdout1, iostderr1 = ssh.exec_command(cmdIO)
        iostderr = iostderr1.read()
        io = iostdout1.read()
        ioread_count = io.read_count #读IO数
        iowrite_count = io.write_count #写IO数
        ioread_bytes = io.read_bytes #IO写字节数
        iowrite_bytes = io.write_bytes #IO读字节数
        #ioread_time = io.read_time #磁盘读时间
        #iowrite_time = io.write_time #磁盘写时间
        Io(times=times,read_count=ioread_count,write_count=iowrite_count,read_bytes=ioread_bytes,write_bytes=iowrite_bytes).save()

        #获取网络信息-------------------------------------------------------------------------
        cmdnet = "NET=`python -c 'import psutil;psutil.psutil.net_io_counters()'`;echo $NET"
        netstdin1, netstdout1, netstderr1 = ssh.exec_command(cmdnet)
        net = netstdout1.read()
        netbytes_sent = net.bytes_sent #发送字节数
        netbytes_recv = net.bytes_recv #接收字节数
        netpackets_sent = net.packets_sent #发送数据包数
        netpackets_recv = net.packets_recv #接收数据包数
        #neterrin = net.terrin #
        #neterrout = net.errout #发送数据包错误的总数
        #netdropin = net.dropin #接收时丢弃的数据包的总数
        #netdropout = net.dropout #发送时丢弃的数据包的总数(OSX和BSD系统总是0)
        net_bytes = netbytes_recv - netbytes_sent #接收字节数 - 发送字节数
        net_packets = netpackets_recv - netpackets_sent #接收数据包数 - 发送数据包数
        Net(times=times,net_bytes=net_bytes,net_packets=net_packets).save()

        cpuresult = Cpu.objects.order_by('-times').all()[0:9]
        memresult = Mem.objects.order_by('-times').all()[0:9]
        ioresult = Io.objects.order_by('-times').all()[0:9]
        netresult = Net.objects.order_by('-times').all()[0:9]
        contant = {'cpuresult':cpuresult,'memresult':memresult,'ioresult':ioresult,'netresult':netresult}

        #CPU与磁盘的报警系统-----------------------------------------------------------------------------------------------------------------------
        url = 'https://oapi.dingtalk.com/robot/send?access_token=0138b8bdea76584c9572e589bd0a372bd61a67bf8d2f6e4553f1b0eaab1fd52e'
        differmem = memused/memtotal*100
        dmeme = math.trunc(differmem) #系统已使用的内存与总内存的比
        if dmeme >= 80:
                p_status = "系统内存已使用比超过80%"
                time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                p_name = IP
                data = {
                        "msgtype": "markdown",
                        "markdown": {
                                "title": "内存告警",
                                "text": "#### %s \n " % time_now +
                                        "> #### 服务器名： %s \n\n " % p_name +
                                        "> #### 状态：%s \n " % p_status +
                                        "> ##### 请尽快处理.........."
                        },
                }
                headers = {'Content-Type': 'application/json;charset=UTF-8'}
                send_data = json.dumps(data).encode('utf-8')
                requests.post(url=url, data=send_data, headers=headers)

        if cpuuser >= 80:
                p_status = "系统磁盘空间超过80%"
                time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                p_name = IP
                data = {
                        "msgtype": "markdown",
                        "markdown": {
                                "title": "磁盘空间告警",
                                "text": "#### %s \n " % time_now +
                                        "> #### 服务器名： %s \n\n " % p_name +
                                        "> #### 状态：%s \n " % p_status +
                                        "> ##### 请尽快处理.........."
                        },
                }
                headers = {'Content-Type': 'application/json;charset=UTF-8'}
                send_data = json.dumps(data).encode('utf-8')
                requests.post(url=url, data=send_data, headers=headers)
        #----------------------------------------------------------------------------------------------------------------------------

        json_data  = serializers.serialize('json',contant)
        json_data = json.loads(json_data)
        if json_data:
                return JsonResponse(json_data,safe=False)
        return render(request,'administration/systeminfo.html')




#获取系统用户的其他信息
@csrf_protect
@login_required(login_url='/login')
def othersys(request):
        if request.method == 'POST':
                IP = request.POST['IP']
                username = request.POST['username']
                passwd = request.POST['passwd']
                times = time.time()

                try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=IP, username=username, password=passwd)
                except Exception:
                        e = '服务器无法连接'
                        contant = {'e': e}
                        json_data = serializers.serialize('json', contant)
                        json_data = json.loads(json_data)
                        return JsonResponse(json_data, safe=False)


                cmdpid = "PIDs=`python -c 'import psutil;psutil.process_iter(attrs=['pid','name'])'`;echo $PIDs"
                pidstdin1, pidstdout1, pidstderr1 = ssh.exec_command(cmdpid)

                pid_list = []
                PIDs = pidstdout1.read()
                for pid in PIDs:
                        Pid = pid.info['pid']
                        Name = pid.info['name']
                        pid_name = Pid + '------>' + Name
                        pid_list.append(pid_name)

                contant = {'pid_list':pid_list}

                json_data = serializers.serialize('json', contant)
                json_data = json.loads(json_data)
                return JsonResponse(json_data, safe=False)
        return render(request,'administration/othersys.html')


#杀死指定的进程
@csrf_protect
@login_required(login_url='/login')
def delpid(request):
        if request.method == 'POST':
                IP = request.POST['IP']
                username = request.POST['username']
                passwd = request.POST['passwd']
                delpids  = request.POST['delpids']

                try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh.connect(hostname=IP, username=username, password=passwd)
                except Exception:
                        e = '服务器无法连接'
                        contant = {'e': e}
                        return render(request, 'adminstration/delpid.html', contant)

                delpidss = delpids.split(',')
                Spid = ''
                sio = StringIO(Spid)
                for pid in delpidss:
                        sio.write( ' ' + pid )
                svaluepid = sio.getvalue()

                cmddel = 'kill -9' +  svaluepid
                pidstdin1, pidstdout1, pidstderr1 = ssh.exec_command(cmddel)
                delpidd = pidstdout1.read()
                if delpidd is None:
                        contant = {'delpidd':'杀死'+svaluepid+'成功'}
                        return render(request, 'adminstration/delpid.html', contant)
                contant = {'delpidd':delpidd}
                return render(request, 'adminstration/delpid.html', contant)
        return render(request,'adminstration/delpid.html')





