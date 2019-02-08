from mongoengine import connect
connect('administration',host='localhost',port=27017)

from mongoengine import *
import time


#存储CPU的信息
class Cpu(Document):
    user = IntField(default=0)
    times = IntField()

#Cpu(user=1 , times=time.time()).save()


result = Cpu.objects.order_by('-times').all()[0:9]
for i in result:
    print(i)