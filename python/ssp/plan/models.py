#!coding:utf8
from django.db import models
from django.contrib import admin

class Vip(models.Model):
    vip = models.IPAddressField('VIP', primary_key=True)
    m_room = models.CharField('机房', max_length=20,null=True,blank=True)
    vweight = models.IntegerField('权重', max_length=10,null=True,blank=True)

    def __unicode__(self):
        return self.vip

class VipAdmin(admin.ModelAdmin):
    list_display = ('vip', 'm_room', 'vweight')
    search_fields = ['vip', 'm_room']
    list_filter = ['m_room']

admin.site.register(Vip, VipAdmin)

class PlanHistory(models.Model):
    PID = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=20,null=True,blank=True)
    status = models.CharField(max_length=1,choices=(('y','成功'),('n','失败')))
    date = models.CharField(max_length=50)

    class Meta:
        ordering = ['-PID']