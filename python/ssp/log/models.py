from django.db import models
from django.contrib import admin

class CRoom(models.Model):
    """docstring for CRoom"""
    ip = models.IPAddressField()
    name = models.TextField()

    class Meta:
        """docstring for Meta"""
        ordering = ('-ip',)
    
    def __unicode__(self):
        return self.name

class DpoolLog(models.Model):
    ip = models.IPAddressField()
    type = models.IntegerField(max_length=4)
    info = models.TextField()
    croom = models.ForeignKey(CRoom)

    class Meta:
        """docstring for Meta"""
        ordering = ('-ip',)
    
    def __unicode__(self):
        return self.ip

    def sina_dpool(self):
        return 'zjzj'+self.ip
    # sina_dpool.admin_order_field = 'croom'
    # sina_dpool.boolean = True
    # sina_dpool.short_description = 'oooddd'

class DpoolLogAdmin(admin.ModelAdmin):
    """docstring for DpoolLogAdmin"""
    list_display = ('ip', 'type', 'info', 'croom', 'sina_dpool')
    # fields = ['ip', 'type']
    # fields = ['ip']
    fieldsets = [
        ('kk',          {'fields':['ip']}),
        ('Date Info',   {'fields':['type','info'],'classes':['collapse']}),
        ('Act',   {'fields':['croom'], 'classes':['collapse']}),
    ]
    list_filter = ['ip', 'info']
    search_fields = ['ip']
        
class DpoolLogInline(admin.TabularInline):
# class DpoolLogInline(admin.StackedInline):
    """docstring for DpoolLogInline"""
    model = DpoolLog
    extra = 4

class CRoomAdmin(admin.ModelAdmin):
    """docstring for CRoomAdmin"""
    list_display = ('ip', 'name')
    inlines = [DpoolLogInline]
        
admin.site.register(DpoolLog, DpoolLogAdmin)
admin.site.register(CRoom, CRoomAdmin)



#!coding:utf8
# from django.db import models
# from django.contrib import admin

# class Device(models.Model):
#     i_ip = models.IPAddressField(primary_key=True)
#     o_ip = models.IPAddressField(null=True,blank=True)
#     hostname = models.CharField(max_length=50)
#     serial_number = models.CharField(max_length=20)
#     cpu_num = models.IntegerField(max_length=4)
#     mem_size = models.IntegerField(max_length=4)
#     disk_size = models.CharField(max_length=8)
#     m_room = models.CharField(max_length=20,null=True,blank=True)
#     app = models.CharField(max_length=20)
#     role = models.CharField(max_length=20)
#     local = models.CharField(max_length=5,choices=(('s','sourth'),('n','north')))
#     status =models.CharField(max_length=1, choices=(('y','active'), ('n', 'inactive')))

#     def app_list(self, appname):
#         devices = Device.objects.filter(app=appname)
#         return devices
    
#     def __unicode__(self):
#         return self.i_ip
        
# class DPW(models.Model):
#     device = models.ForeignKey(Device)
#     port = models.IntegerField(max_length=4)
#     weight = models.IntegerField(max_length=4)

#     def __getinfo(self):
#         info = "%s:%s,%s" % (self.device.o_ip, self.port, self.weight)
#         return info
    
#     def __unicode__(self):
#         return self.__getinfo()
#         # return self.device.o_ip

# class Pool(models.Model):
#     name = models.CharField(max_length=20,null=True,blank=True)
#     dpw = models.ManyToManyField(DPW)
    
#     def __unicode__(self):
#         return self.vip

# class Vip(models.Model):
#     vip = models.IPAddressField()
#     pool = models.ForeignKey(Pool)
#     m_room = models.CharField(max_length=20,null=True,blank=True)
    
#     def __unicode__(self):
#         return self.vip
    
# class Domain(models.Model):
#     domain = models.CharField(max_length=50)
#     vip = models.ManyToManyField(Pool)

#     def __unicode__(self):
#         return self.domain

# admin.site.register(DPW)