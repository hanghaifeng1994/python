"""
Django settings for operation project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(0x$4-xc7c_uem)$%c0xqcp9!+--8!+ih=0nxifxda@(omx^o3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

#应用（项目）
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'security',
    'administration',
    'appManager',
    'DBA',
    'ADS',
    'autoest',
    'business',
]

#中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.myMiddle.MyMiddle',#添加一个自定义中间件

]

ROOT_URLCONF = 'operation.urls'

#应用访问的路径
SITE_URL = '/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'operation.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

#连接mysql数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
        'NAME': 'operation',                   # 数据库名
        'USER': 'root',                        # 你的数据库user
        'PASSWORD': '',                        # 你的数据库password
        'HOST': 'localhost',                   # 开发的时候，使用localhost
        'PORT': '3306',                        # 默认3306
    },

}

#连接mongodb数据库
from mongoengine import connect
connect('administration',host='localhost',port=27017)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'jumpserver.context_processors.name_proc',
)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'#改为了简体中文

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

#加载静态文件
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

#用redis数据库缓存session数据后，mysql就不会在存储session数据
import redis_sessions
#用redis缓存session
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIST_DB = 0 #有16库，用第0个库
SESSION_REDIS_PASSWORD = ""
SESSION_REDIS_PREFIX = 'session'


#配置celery,python 并发分布式框架
import djcelery
#初始化队列
djcelery.setup_loader()
#连接redis数据库
BROKER_URL = 'redis://localhost:6379/0'#在Celery执行过程中的数据支持。保存列队记录、执行记录等等。
#引入任务路径
CELERY_IMPORTS = ()
#设置时区
CELERY_TIMEZONE = TIME_ZONE


#下面是定时任务的设置：
from celery.schedules import crontab
from datetime import timedelta
#定义定时任务：
CELERYBEAT_SCHEDULE = {

}
