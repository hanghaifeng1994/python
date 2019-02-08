from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from common.mymako import render_json
from IPy import IP
import pycurl
import os
from .models import *
import json


#输出指定网段的所有IP清单
@csrf_protect
@login_required(login_url='/login')
def iplen(request):
    if request.mehtod == 'POST':
        IPlen = request.POST['IPlen']
        ip = IP(IPlen)

        ips = ip.len()
        iplist = [] #输出指定网段的IP个数
        for x in ip:
            iplist.append(x)
        contant = {'iplen':iplist,'ips':ips}
        json_data = serializers.serialize('json', contant)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)
    return render(request,'business/iplen.html')


#根据输入的IP或子网返回网络，掩码，广播，反向解析，子网数，IP类型等信息
@csrf_protect
@login_required(login_url='/login')
def ipinput(request):
    if request.method == 'POST':
        ipnet = request.POST['ipnet']
        ips = IP(ipnet)
        #为一个网络地址
        if len(ips) > 1:
            net = ips.net() #输出网络地址
            mask = ips.netmask() #输出网络掩码地址
            cast = ips.broadcast() #输出网络广播地址
            names = ips.reverseNames()[0] #输出地址反向解析
            len = len(ips) #输出网络子网数
            Net(ipnets=ipnet,net=net,mask=mask,cast=cast,names=names,len=len)
        # 为单个IP地址
        else:
            enames = ips.reverseNames()[0] #输出IP反向解析
            ehex = ips.strHex() #输出十六进制地址
            ebin = ips.strBin() #输出二进制地址
            etype = ips.iptype() #输出地址类型
            Ip(ipnets=ipnet,ename=enames,ehex=ehex,ebin=ebin,etype=etype)

        contant1 = {'net':net,'mask':mask,'cast':cast,'names':names,'len':len}
        contant2 = {'enames':enames,'ehex':ehex,'ebin':ebin,'etype':etype}

        if len(contant1) > 1:
            json_data = serializers.serialize('json', contant1)
            json_data = json.loads(json_data)
            return JsonResponse(json_data, safe=False)
        if len(contant2) > 1:
            json_data = serializers.serialize('json', contant2)
            json_data = json.loads(json_data)
            return JsonResponse(json_data, safe=False)
    return render(request,'business/ipinput.html')


#探测Web服务质量
@csrf_protect
@login_required(login_url='/login')
def pyweb(request):
    if request.method == 'POST':
        url = request.POST['url']
        c = pycurl.Curl()
        c.setopt(pycurl.URL,url)
        c.setopt(pycurl.CONNECTTIMEOUT,5)
        c.setopt(pycurl.TIMEOUT,5)
        c.setopt(pycurl.NOPROGRESS,1)
        c.setopt(pycurl.FORBID_REUSE,1)
        c.setopt(pycurl.MAXREDIRS,1)
        c.setopt(pycurl.DNS_CACHE_TIMEOUT,30)
        indexfile = open(os.path.dirname('businessFile/')+url+".text",'wb') ##############################################
        c.setopt(pycurl.WRITEHEADER,indexfile)
        c.setopt(pycurl.WRITEDATA,indexfile)
        try:
            c.perform() #提交请求
        except Exception as e:
            err = 'connection error:'+str(e)
            contant = err
            indexfile.close()
            return render(request,'business/pyweb.html',contant)

        NAMEELOOKKUP_TIME = c.getinfo(c.NAMELOOKUOP_TIME) #获取DNS解析时间
        CONNECT_TIME = c.getinfo(c.PRETRASFER_TIME) #获取建立连接时间
        PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME) #获取从建立连接到准备传输所消耗的时间
        STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME) #获取从建立连接到传输开始消耗的时间
        TOTAL_TIME = c.getinfo(c.TOTAL_TIME) #获取传输的总时间
        HTTP_CODE = c.getinfo(c.HTTP_CODE) #获取HTTP状态码
        SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD) #获取下载数据包大小
        HEADER_SIZE = c.getinfo(c.HEADER_SIZE) #获取HTTP头部大小
        SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD) #获取平均下载速度

        PyWb(url=url,NAMEELOOKKUP_TIME=NAMEELOOKKUP_TIME,CONNECT_TIME=CONNECT_TIME,
             PRETRANSFER_TIME=PRETRANSFER_TIME,STARTTRANSFER_TIME=STARTTRANSFER_TIME,TOTAL_TIME=TOTAL_TIME,HTTP_CODE=HTTP_CODE,SIZE_DOWNLOAD=SIZE_DOWNLOAD,
             HEADER_SIZE=HEADER_SIZE,SPEED_DOWNLOAD=SPEED_DOWNLOAD).save()

        contant = {'NAMEELOOKKUP_TIME':NAMEELOOKKUP_TIME,'CONNECT_TIME':CONNECT_TIME,'PRETRANSFER_TIME':PRETRANSFER_TIME,
                   'STARTTRANSFER_TIME':STARTTRANSFER_TIME,'TOTAL_TIME':TOTAL_TIME,'HTTP_CODE':HTTP_CODE,'SIZE_DOWNLOAD':SIZE_DOWNLOAD,'HEADER_SIZE':HEADER_SIZE,'SPEED_DOWNLOAD':SPEED_DOWNLOAD}
        #关闭文件及Curl对象
        indexfile.close()
        c.close()

        json_data = serializers.serialize('json', contant)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)
    return render(request, 'business/pyweb.html')








