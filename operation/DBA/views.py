from django.shortcuts import render

# Create your views here.
import paramiko
import re
import threading


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from concurrent.futures import ThreadPoolExecutor,as_completed,wait,ALL_COMPLETED,FIRST_COMPLETED
import pexpect
import sys
import time



#安装VNC环境准备，请在win系统上安装VNC客户端,需要提前安装pexpect
@csrf_protect
@login_required(login_url='/login')
def orlvnc(request):
    if request == 'POST':
        IP = request.POST['IP']
        username = request.POST['username']
        passwd = request.POST['passwd']
        VNCname = request.POST['VNCname']
        VNCpasswd = request.POST['VNCpasswd']

        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        child = pexpect.spawn('ssh root@ '+IP)
        #将相应的日志写入到相应的文件中
        fount = open('VNC-'+IP+'-'+time_now+'.txt','w')
        child.logfile = fount

        child.expect('passworld:')
        child.sendline(passwd)

        child.expect('#')
        child.sendline('yum check-update')
        child.expect('#')
        child.sendline('yum groupinstall "X Window System"')
        child.expect('#')
        child.sendline('yum install gnome-classic-session gnome-terminalnautilus-open-terminal control-center liberation-mono-fonts tigervnc-server ')
        child.expect('#')
        child.sendline('unlink /etc/systemd/system/default.target')
        child.expect('#')
        child.sendline(' ln -sf /lib/systemd/system/graphical.target/etc/systemd/system/default.target')
        #配置VNC文件
        child.expect('#')
        child.sendline('cp /lib/systemd/system/vncserver@.service  /etc/systemd/system/vncserver@:1.service')
        #编辑/etc/sysconfig/vncservers文件
        child.expect('#')
        child.sendline("echo 'VNCSERVERS=\"1:root\"'>>/etc/sysconfig/vncservers;echo 'VNCSERVERARGS[1]=\"-geometry800x600\"'>>/etc/sysconfig/vncservers")
        #修改/etc/systemd/system/vncserver@:1.service文件
        child.expect('#')
        child.sendline("sed -i 's/<USER>/root/g' /etc/systemd/system/vncserver@:1.service")
        child.expect('#')
        child.sendline('systemd')
        child.expect('#')
        child.sendline('systemctl daemon-reload')
        child.expect('#')
        child.sendline('vncpasswd')
        child.expect('Password:')
        child.sendline(VNCname)
        child.expect('Verify:')
        child.sendline(VNCpasswd)
        child.expect('Would you like to enter a view-only password (y/n)?')
        child.sendline('y')
        child.expect('Password:')
        child.sendline(VNCname)
        child.expect('Verify:')
        child.sendline(VNCpasswd)
        #永久开启VNC服务
        child.expect('#')
        child.sendline('systemctl enable vncserver@1.service')
        #关闭防火墙
        child.expect('#')
        child.sendline('setenforce 0')
        child.expect('#')
        child.sendline('systemctl stop firewalld.service')
        child.expect('#')
        child.sendline('systemctl disable firewalld.service ')

        contant = {'vnc':'vnc的环境配置完毕，请查看对应的日志'}
        return render(request,'DBA/orlvnc.html',contant)
    return render(request, 'DBA/orlvnc.html')






#自动部署oracle数据库安装环境
@csrf_protect
@login_required(login_url='/login')
def autooracle(request):
    if request.method == 'POST':
        IP = request.POST['IP']
        username = request.POST['username']
        passwd = request.POST['passwd']
        pathorls = request.POST['pathorls']
        orlpasswd = request.POST['orlpasswd']

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=IP, username=username, password=passwd)
        except Exception:
            e = '服务器无法连接'
            contant = {'e': e}
            return render(request, 'DBA/autooracle.html', contant)

        #1.判断系统磁盘的空间是否足够用来安装oracel
        #----------------------------------------------------------------------------
        cmddf = "df -h | sed -n '2p' | awk '{print $3}'"
        dfstdin1, dfstdout1, dfstderr1 = ssh.exec_command(cmddf)
        df = dfstdout1.read()
        dff = re.findall('G',df)
        if dff is not None:
            dfhllist = re.findall('\d|[\d+\.\d]', df)
            dfhstr = ''.join(dfhllist)
            dff = float(dfhstr)
            if dff < 8:
                contant  ={'df':'磁盘空间不足'}
                return render(request,'DBA/autooracle.html',contant)
        #---------------------------------------------------------------------------
        #2.安装oracle需要的软件包：
        #----------------------------------------------------------------------------
        orlpackage1 = 'yum install binutils -y'
        orlpackage2 = 'yum install compat-libcap1 -y'
        orlpackage3 = 'yum install compat-libstdc++-33 -y'
        orlpackage4 = 'yum install gcc -y'
        orlpackage5 = 'yum install gcc-c++ -y'
        orlpackage6 = 'yum install glibc -y'
        orlpackage7 = 'yum install glibc-devel -yyum install ksh -y'
        orlpackage8 = 'yum install libgcc -y'
        orlpackage9 = 'yum install libstdc++ -y'
        orlpackage10 =  'yum install libstdc++-devel -y'
        orlpackage11 = 'yum install libaio -y'
        orlpackage12 = 'yum install libaio-devel -y'
        orlpackage13 = 'yum install libXext -y'
        orlpackage14 = 'yum install libXtst -y'
        orlpackage15 = 'yum install libX11 -y'
        orlpackage16 = 'yum install libXau -y'
        orlpackage17 = 'yum install libxcb -y'
        orlpackage18 = 'yum install libXi -y'
        orlpackage19 = 'yum install make -y'
        orlpackage20 = 'yum install sysstat -y'
        orlpackage21 = 'yum install unixODBC -y'
        orlpackage22 = 'yum install unixODBC-devel -y'
        orlpackages = [orlpackage1,orlpackage2,orlpackage3,orlpackage4,orlpackage5,orlpackage6,orlpackage7,orlpackage8,
                       orlpackage9,orlpackage10,orlpackage11,orlpackage12,orlpackage13,orlpackage14,orlpackage15,
                       orlpackage16,orlpackage17,orlpackage18,orlpackage19,orlpackage20,orlpackage21,orlpackage22]
        class orl(threading.Thread):
            def __init__(self,cmdorl):
                self.cmdorl = cmdorl
                threading.Thread.__init__(self)
            def run(self):
                    orlstdin1, orlstdout1, orlstderr1 = ssh.exec_command(self.cmdorl)
                    orlread = orlstdout1.read()
                    yield orlread
        orlouts = []
        for orlpackage in orlpackages:
            orlout = orl(orlpackage)
            orlouts.append(orlout)
            for orlthread1 in orlouts:
                orlyield = orlthread1.start()
            for orlthread2 in orlouts:
                orlthread2.join()
        orlList = list(orlyield)
        #------------------------------------------------------------------------------
        #3.关闭防火墙
        #--------------------------------------------------------------------------------------
        cmdfir = 'chkconfig iptables off;systemctl stop firewalld;setenforce 0'
        firstdin1, firstdout1, firstderr1 = ssh.exec_command(cmdfir)
        #---------------------------------------------------------------------------------------
        #3.配置/etc/hosts文件
        #-------------------------------------------------------------------------------------
        cmdhosts = "echo '172.26.60.182 db01'>> /etc/hosts"
        hostsstdin1, hostsstdout1, hostsstderr1 = ssh.exec_command(cmdhosts)
        hostserr = hostsstderr1.read()
        if hostserr != None:
            contant = {'hosterr':hostserr}
            return render(request,'DBA/autooracle.html',contant)
        #--------------------------------------------------------------------------------------
        #4.设置hostname值
        #--------------------------------------------------------------------------------------
        cmdname = 'hostnamectl set-hostname db01'
        namestdin1, namestdout1, namestderr1 = ssh.exec_command(cmdname)
        name = namestderr1.read()
        if name is not None:
            err = '设置hostname值失败'
            contant = {'err':err}
            return render(request,'DBA/autooracle.html',contant)
        #--------------------------------------------------------------------------------------
        #5.用线程实现下载oracle数据库的压缩包
        #----------------------------------------------------------------------------
        pathorllist = pathorls.split(',')
        def path(pathorls):
                cmdpath = 'wget ' + '-P /home '+ pathorls
                orlstdin1, orlstdout1, orlstderr1 = ssh.exec_command(cmdpath)
                orl = orlstdout1.read()
                yield orl
        executor = ThreadPoolExecutor(max_workers=4)
        all_task = [executor.submit(path,(pathorls)) for pathorls in pathorllist]
        wait(all_task,return_when=ALL_COMPLETED)
        #-----------------------------------------------------------------------------
        #6.解压oracle的压缩文件
        #------------------------------------------------------------------------------
        orl1 = pathorllist[0].split('/')[-1]
        orl2 = pathorllist[1].split('/')[-1]
        orllist = [orl1,orl2]
        def unziporls(orl):
            cmdunzip = 'cd /home;unzip '+ orl
            unzipstdin1, unzipstdout1, unzipstderr1 = ssh.exec_command(cmdunzip)
            unzip = unzipstdout1.read()
            yield unzip
        executor = ThreadPoolExecutor(max_workers=4)
        all_task1 = [executor.submit(unziporls, (orl)) for orl in orllist]
        wait(all_task1, return_when=ALL_COMPLETED)
        #------------------------------------------------------------------------------
        #6.建立oracle的用户组和用户名
        #-----------------------------------------------------------------------------------
        cmdunzip = '/usr/sbin/groupadd -g 60001 oinstall;/usr/sbin/groupadd -g 60002 dba;/usr/sbin/groupadd -g 60003 oper;useradd oracle;echo '+orlpasswd+' | passwd --stdin oracle;usermod -G oper oracle dba;usermod -G oper oracle;usermod -G oper dba'
        unzipstdin1, unzipstdout1, unzipstderr1 = ssh.exec_command(cmdunzip)
        unziperr = unzipstderr1.read()
        if unziperr != None:
            contant = {'unziperr':unziperr}
            return render(request,'DBA/autooracle.html',contant)
        #-------------------------------------------------------------------------------------
        #7.创建oracle目录和授权
        #---------------------------------------------------------------------------------------
        cmddir = 'mkdir -p /oracle/product/11.2.0/dbhome_1;chown -R oracle:oinstall /oracle;chomd -R 775 /oracle'
        dirstdin1, dirstdout1, dirstderr1 = ssh.exec_command(cmddir)
        #----------------------------------------------------------------------------------------
        #8.修改/etc/security/limits.conf文件
        #--------------------------------------------------------------------------------------
        cmdlimit = "echo 'oracle soft nproc 2047'>>/etc/security/limits.conf;echo 'oracle hard nproc 16384'>>/etc/security/limits.conf;" \
                   "echo 'oracle soft nofile 1024'>>/etc/security/limits.conf;echo 'oracle hard nofile 65536'>>/etc/security/limits.conf;" \
                   "echo 'oracle soft stack 10240'>>/etc/security/limits.conf;echo 'oracle hard stack 32768'>>/etc/security/limits.conf"
        limitstdin1, limitstdout1, limitstderr1 = ssh.exec_command(cmdlimit)
        #--------------------------------------------------------------------------------------
        #9.修改/etc/security/limits.d/20-nproc.conf文件
        #------------------------------------------------------------------------------------------
        cmdconf = "echo '* - nproc 16384'>>/etc/security/limits.d/20-nproc.conf"
        confstdin1, confstdout1, confstderr1 = ssh.exec_command(cmdconf)
        #------------------------------------------------------------------------------------------
        #10.修改/etc/pam.d/login文件
        #-------------------------------------------------------------------------------------------
        cmdlogin = "echo 'session required /lib/security/pam_limits.so'>>/etc/pam.d/login;echo 'session required pam_limits.so'>>/etc/pam.d/login"
        loginstdin1, loginstdout1, loginstderr1 = ssh.exec_command(cmdlogin)
        #-------------------------------------------------------------------------------------------
        #11.修改/etc/sysctl.conf文件，使其生效
        #------------------------------------------------------------------------------------------
        cmdsysctl = "echo 'fs.aio-max-nr = 1048576'>>/etc/sysctl.conf;echo 'fs.file-max = 6815744'>>/etc/sysctl.conf;echo 'kernel.shmmax = 8589934592'>>/etc/sysctl.conf;" \
                    "echo 'kernel.shmall = 2097152'>>/etc/sysctl.conf;echo 'kernel.shmmni = 4096'>>/etc/sysctl.conf;echo 'kernel.sem = 250 32000 100 128'>>/etc/sysctl.conf;" \
                    "echo 'net.ipv4.ip_local_port_range = 9000 65500'>>/etc/sysctl.conf;echo 'net.core.rmem_default = 262144'>>/etc/sysctl.conf;echo 'net.core.rmem_max = 4194304'>>/etc/sysctl.conf;" \
                    "echo 'net.core.wmem_default = 262144'>>/etc/sysctl.conf;echo 'net.core.wmem_max = 1048586'>>/etc/sysctl.conf;sysctl -p"
        sysstdin1, sysstdout1, sysstderr1 = ssh.exec_command(cmdsysctl)
        #--------------------------------------------------------------------------------------------
        #切换到oracle用户，设置bash_profile文件
        #--------------------------------------------------------------------------------------------
        cmdbash = "su - oracle;echo 'TMP=/tmp; export TMP'>>/home/oracle/.bash_profile;echo 'TMPDIR=$TMP; export TMPDIR'>>/home/oracle/.bash_profile;" \
                  "echo 'ORACLE_BASE=/oracle/; export ORACLE_BASE'>>/home/oracel/.bash_profile;echo 'ORACLE_HOME=$ORACLE_BASE/product/11.2.0; export ORACLE_HOME'>>/home/oracle/.bash_profile;" \
                  "echo 'ORACLE_SID=orcl; export ORACLE_SID'>>/home/oracel/.bash_profile;echo 'ORACLE_TERM=xterm; export ORACLE_TERM'>>/home/oracel/.bash_profile;" \
                  "echo 'PATH=/usr/sbin:$PATH; export PATH'>>/home/oracel/.bash_profile;echo 'PATH=$ORACLE_HOME/bin:$PATH; export PATH'>>/home/oracel/.bash_profile;" \
                  "echo 'LD_LIBRARY_PATH=$ORACLE_HOME/lib:/lib:/usr/lib; export LD_LIBRARY_PATH'>>/home/oracel/.bash_profile; export PATH;echo 'CLASSPATH=$ORACLE_HOME/JRE:$ORACLE_HOME/jlib:$ORACLE_HOME/rdbms/jlib; export CLASSPATH'>>/home/oracel/.bash_profile;" \
                  "echo 'NLS_DATE_FORMAT=\"yyyy-mm-dd HH24:MI:SS\"; export NLS_DATE_FORMAT'>>/home/oracel/.bash_profile;echo 'NLS_LANG=AMERICAN_AMERICA.ZHS16GBK;export NLS_LANG'>>/home/oracel/.bash_profile;" \
                  "echo 'if [ $USER = \"oracle\" ] || [ $USER = \"grid\" ]; then'>>/home/oracel/.bash_profile;echo 'if [ $SHELL = \"/bin/ksh\" ]; then'>>/home/oracel/.bash_profile" \
                   "echo 'ulimit -p 16384'>>/home/oracel/.bash_profile;echo 'ulimit -n 65536'>>/home/oracel/.bash_profile;echo 'else'>>/home/oracel/.bash_profile;echo 'ulimit -u 16384 -n 65536'>>/home/oracel/.bash_profile" \
                   "echo 'fi'>>/home/oracel/.bash_profile;echo 'umask 022'>>/home/oracel/.bash_profile;echo 'fi'>>/home/oracel/.bash_profile"
        basgstdin1, bashstdout1, bashstderr1 = ssh.exec_command(cmdbash)
        #--------------------------------------------------------------------------------------------------
        #为orcale安装包授权：
        #-------------------------------------------------------------------------------------------------
        cmdch = "chown -R oracle:oinstall /home/database;chmod -R 755 /home/database"
        chstdin1, chstdout1, chstderr1 = ssh.exec_command(cmdch)
        #--------------------------------------------------------------------------------------
        #创建oraInventoy , 使其生效
        #-------------------------------------------------------------------------------------------------------
        cmdora = "mkdir /oraInventory;chown -R oracle:oinstall /oraInventory;cd /oraInventory;./orainstRoot.sh;/oracle/product/11.2.0/dbhome_1/root.sh;./orainstRoot.sh;/oracle/product/11.2.0/dbhome_1/root.sh"
        orastdin1, orastdout1, orastderr1 = ssh.exec_command(cmdora)
        #-------------------------------------------------------------------------------------------------------------------
        #重启服务器
        #-------------------------------------------------------------
        cmdreboot = "reboot"
        restdin1, restdout1, restderr1 = ssh.exec_command(cmdreboot)
        #----------------------------------------------------------------
        contant = {'end':'oracel安装环境准备成功'}
        return render(request,'DBA/autooracle.html',contant)
    return render(request,'DBA/autooracle.html')




#迁移oracle数据库中的数据,你需要使用
def removeorl(request):
    if request.method == 'POST':
        IP = request.POST['IP']
        username = request.POST['username']
        passwd = request.POST['passwd']
        toorlname = request.POST['orlname']
        toorlpasswd = request.POST['orlpasswd']
        uporlname = request.POST['uporlname']
        uporlpasswd = request.POST['uporlpasswd']
        orlusers = request.POST['orlusers']

        orluserlist = orlusers.split(',')

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=IP, username=username, password=passwd)
        except Exception:
            e = '服务器无法连接'
            contant = {'e': e}
            return render(request, 'DBA/removeorl.html', contant)

        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        p = time_now.split(' ')
        o = p[0].split('-')
        j = ''.join(o)

        def to(orlsuser):
            cmdto = "exp "+toorlname+"/"+toorlpasswd+"@orcl owner="+orlsuser+" rows=y indexes=n compress=n buffer=65536 feedback=100000 file=/exp_hbddlms.dmp log=/exp_"+j+".log"
            tostdin1, tostdout1, tostderr1 = ssh.exec_command(cmdto)
            tolist = tostdout1.read()
            yield tolist
        executor = ThreadPoolExecutor(max_workers=4)
        all_task = [executor.submit(to,(orlsuser)) for orlsuser in orluserlist]
        wait(all_task,return_when=ALL_COMPLETED)


        child = pexpect.spawn('ssh root@ ' + IP)
        # 将相应的日志写入到相应的文件中
        fount = open('VNC-' + IP + '-' + time_now + '.txt', 'w')
        child.logfile = fount
        child.expect('passworld:')
        child.sendline(passwd)

        child.expect('#')
        child.sendline('scp /exp_'+j+'.log root@'+IP)

        child.expect('#')
        child.sendline(uporlpasswd)

        child.expect('#')
        contant = {'to':'迁移数据成功，请查看对应的日志文件'}
        return render(request,'DBA/removeorl.html',contant)
    return render(request,'DBA/removeorl.html')




#备份oracle数据库：
#def backorl(request):




#安装mysql数据库：
#def automysql(request):




#迁移mysql数据库
#def removesql


#备份mysql数据库
#def backsql(request):














