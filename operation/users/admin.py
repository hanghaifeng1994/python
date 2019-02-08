from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CommonerUser

# Register your models here.


#Inline是将User与普通会员表一起显示
class CommonerUserInline(admin.TabularInline):
    model = CommonerUser
    can_delete = False
    verbose_name_plural = '普通会员表'

#定义后台User的后台管理页面
class UserAdmin(BaseUserAdmin):
    inlines = (CommonerUserInline,)


admin.site.unregister(User)
admin.site.register(User,UserAdmin)


