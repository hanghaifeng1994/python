from django.db import models

# Create your models here.
from mongoengine import *


#存储CPU的信息
class Cpu(Document):
    times = IntField()
    user = IntField(default=0)



#存储系统内存的信息
class Mem(Document):
    times = IntField()
    total = IntField(default=0)
    used = IntField(default=0)
    free = IntField(default=0)



#硬盘IO的信息
class Io(Document):
    times = IntField()
    read_count = IntField(default=0)
    write_count = IntField(default=0)
    read_bytes = IntField(default=0)
    write_bytes = IntField(default=0)



#网络信息存储
class Net(Document):
    times = IntField()
    net_bytes = IntField(default=0)
    net_packets = IntField(default=0)




