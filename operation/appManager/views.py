from django.shortcuts import render


import psutil
import os
import request
import json
import time
import paramiko
import requests
from common.mymako import render_json

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect



#��Ӧ��״̬���м��
@csrf_protect
@login_required(login_url='/login')
def appControl(request):
    if request.method == 'POST':
        IP = request.POST['IP']
        username = request.POST['username']
        passwd = request.POST['passwd']
        apps = request.POST['apps']

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=IP, username=username, password=passwd)
        except Exception:
            e = '�������޷�����'
            contant = {'e': e}
            return render(request, 'adminstration/inputinfo.html', contant)

        url = 'https://oapi.dingtalk.com/robot/send?access_token=0138b8bdea76584c9572e589bd0a372bd61a67bf8d2f6e4553f1b0eaab1fd52e'
        time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        #Ҫ��صķ��������б�
        app_list = apps.split(',')
        #Ҫ��صķ�����������
        monitor_map = {}
        for app in app_list:
            monitor_map[app] = 'server '+app+' start'

        while True:
            #���з���������pid���ֵ�
            proc_dict = {}
            #���з��������ļ���
            proc_name = set()
            #���Զ��ϵͳ�����������ķ�������
            cmdAPPS = "APPS=`python -c 'import psutil;psutil.process_iter(attrs=['pid','name'])'`;echo $apps"
            appsstdin1, appsstdout1, appsstderr1 = ssh.exec_command(cmdAPPS)
            appsstderr = appsstderr1.read()
            apps = appsstdout1.read()
            for p in apps:
                proc_dict[p.info['pid']] = p.info['name']
                proc_name.add(p.info['name'])

            proc_stop = app_list - proc_name
            states = {}
            if proc_stop:
                for p in proc_stop:
                    p_status = 'ֹͣ'
                    p_name = p

                    data = {
                        "msgtype": "markdown",
                        "markdown": {
                        "title":"���ѶϢ",
                        "text":"#### %s \n " % time_now +
                               "> #### ���������� %s \n\n " % p_name +
                               "> #### ״̬��%s \n " % p_status +
                               "> ##### ���ڳ�������"
                        },
                    }
                    headers = {'Content-Type': 'application/json;charset=UTF-8'}
                    send_data = json.dumps(data).encode('utf-8')
                    requests.post(url=url, data=send_data, headers=headers)

                    #����ֹͣ�ķ�����
                    cmdstart = monitor_map[p]
                    startstdin1, startstdout1, startstderr1 = ssh.exec_command(cmdstart)
                    start =  startstdout1.read()

                    #�ٴμ��Զ��ϵͳ�����������ķ�������
                    rproc_name = set()
                    cmdAPPS = "APPS=`python -c 'import psutil;psutil.process_iter(attrs=['pid','name'])'`;echo $apps"
                    appsstdin1, appsstdout1, appsstderr1 = ssh.exec_command(cmdAPPS)
                    appsstderr = appsstderr1.read()
                    apps = appsstdout1.read()
                    for p in apps:
                        rproc_name.add(p.info['name'])

                    if p in rproc_name:
                        p_status = '����'
                        data = {
                            "msgtype": "markdown",
                            "markdown": {
                                "title": "���ѶϢ",
                                "text": "#### %s \n " % time_now +
                                        "> #### ���������� %s \n\n " % p_name +
                                        "> #### ״̬��%s \n " % p_status +
                                        "> ##### �����ɹ�"
                            },
                        }
                        headers = {'Content-Type': 'application/json;charset=UTF-8'}
                        send_data = json.dumps(data).encode('utf-8')
                        requests.post(url=url, data=send_data, headers=headers)

                    else:
                        p_status = 'ֹͣ'
                        data = {
                            "msgtype": "markdown",
                            "markdown": {
                                "title": "���ѶϢ",
                                "text": "#### %s \n " % time_now +
                                        "> #### ���������� %s \n\n " % p_name +
                                        "> #### ״̬��%s \n " % p_status +
                                        "> ##### ����ʧ��"
                            },
                        }
                        headers = {'Content-Type': 'application/json;charset=UTF-8'}
                        send_data = json.dumps(data).encode('utf-8')
                        requests.post(url=url, data=send_data, headers=headers)

                    states[p] = p_name #�洢����Ӧ�õ�״̬

                time.sleep(2)
            contant = {'states': states}
            return render(request,'appManager/appsManager.html',render_json(contant))
    return render(request,'appManage/inputinfos.html')









