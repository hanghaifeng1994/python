from django.db import models

# Create your models here.


from mongoengine import *

class Net(Document):
    ipnet = StringField(max_length=16)
    net = StringField(max_length=16)
    mask = StringField(max_length=16)
    cast = StringField(max_length=16)
    names = StringField(max_length=16)
    len = StringField(max_length=16)


class Ip(Document):
    ipnet = StringField(max_length=16)
    enames = StringField(max_length=16)
    ehex = StringField(max_length=16)
    ebin = StringField(max_length=16)
    etype = StringField(max_length=16)


class PyWb(Document):
    url = StringField(max_length=16)
    NAMEELOOKKUP_TIME = StringField(max_length=16)
    CONNECT_TIME = StringField(max_length=16)
    PRETRANSFER_TIME = StringField(max_length=16)
    STARTTRANSFER_TIME = StringField(max_length=16)
    TOTAL_TIME = StringField(max_length=16)
    HTTP_CODE = StringField(max_length=16)
    SIZE_DOWNLOAD = StringField(max_length=16)
    HEADER_SIZE = StringField(max_length=16)
    SPEED_DOWNLOAD = StringField(max_length=16)
