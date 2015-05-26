#!coding:utf8
from django.db import models
from django.contrib import admin
import re

class Device(models.Model):
    i_ip             =models.IPAddressField('内网IP', primary_key=True)
    o_ip             =models.IPAddressField('外网IP', null=True,blank=True)
    hostname         =models.CharField('主机名', max_length=50)
    serial_number    =models.CharField('盘点号', max_length=20)
    cpu_num          =models.IntegerField('cpu核心数', max_length=4)
    mem_size         =models.IntegerField('内存大小', max_length=4)
    disk_size        =models.CharField('硬盘大小', max_length=8)
    m_room           =models.CharField('机房', max_length=20,null=True,blank=True)
    app              =models.CharField('业务名称', max_length=20)
    role             =models.CharField('角色', max_length=20)
    local            =models.CharField('南方/北方', max_length=5,choices=(('s','sourth'),('n','north')))
    status           =models.CharField('状态', max_length=1, choices=(('y','active'), ('n', 'inactive')))
    remark           =models.TextField('备注', max_length=200,null=True,blank=True)

    def get_all_host(self, appname):
        devices = Device.objects.filter(app=appname).order_by('m_room')
        return devices

    def search_host(self, search_fields):
        search_re = re.compile(r"\d+\.\d+\.\d+\.\d+")
        if search_re.findall(search_fields):
            devices = Device.objects.filter(i_ip=search_fields).order_by('m_room')
            if devices:
                search_devices = devices
            else:
                search_devices = Device.objects.filter(o_ip=search_fields).order_by('m_room')
        else:
            search_devices = Device.objects.filter(hostname=search_fields).order_by('m_room')

        return search_devices
    
    def __unicode__(self):
        return self.i_ip

class DeviceAdmin(admin.ModelAdmin):
    """docstring for DeviceAdmin"""
    list_display = ('i_ip', 'o_ip', 'hostname', 'm_room', 'app')
    # fields = ['ip', 'type']
    # fields = ['ip']
    fieldsets = [
        ('唯一标示',          {'fields':['i_ip', 'o_ip', 'hostname']}),
        ('服务器信息',   {'fields':['serial_number','cpu_num', 'mem_size', 'disk_size', 'status']}),
        ('应用',   {'fields':['app', 'role']}),
        ('位置信息',   {'fields':['m_room', 'local']}),
        ('备注',   {'fields':['remark'], 'classes':['collapse']})
    ]
    list_filter = ['app', 'm_room', 'role']
    search_fields = ['i_ip', 'o_ip', 'hostname']

admin.site.register(Device, DeviceAdmin)
    
class Domain(models.Model):
    dname         =models.CharField('域名', max_length=60)
    is_dynamic    =models.IntegerField('动/静', max_length=1, choices=(('1','dynamic'), ('0', 'static')))
    view          =models.CharField('分组', max_length=60)
    type          =models.CharField(max_length=10)
    data          =models.CharField('VIP', max_length=50)#models.IPAddressField()有的记录data为域名而不是ip，例如data_0': [u'freemx.sinamail.sina.com.cn.']
    app           =models.CharField('业务名称', max_length=100)
    status        =models.NullBooleanField('状态')
    dweight       =models.FloatField('权重', null=True,blank=True)

    def __unicode__(self):
        return self.dname

class DomainAdmin(admin.ModelAdmin):
    """docstring for DomainAdmin"""
    list_display = ('dname', 'view', 'data', 'dweight', 'status')
    list_filter = ['dname']
    search_fields = ['dname', 'view']

admin.site.register(Domain, DomainAdmin)


class VieWeight(models.Model):
    """设置城市和运营商流量权重"""
    view      = models.CharField('城市/运营商/区域', primary_key=True, max_length=60)
    weight    = models.FloatField('权重', max_length=10)
    typ      = models.CharField('类型',max_length=20, null=True,blank=True)

class VieWeightAdmin(admin.ModelAdmin):
    list_display = ('view', 'weight', 'typ')
    list_filter = ['typ']
    search_fields = ['view', 'weight', 'typ']

admin.site.register(VieWeight, VieWeightAdmin)
# admin.site.register(Device)