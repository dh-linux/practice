from django.db import models
from django.contrib import admin

class DpoolLog(models.Model):
    ip = models.IPAddressField()
    type = models.IntegerField(max_length=4)
    info = models.TextField()

    class Meta:
        """docstring for Meta"""
        ordering = ('-ip',)
            
    
    def __unicode__(self):
        return self.ip

class DpoolLogAdmin(admin.ModelAdmin):
    """docstring for DpoolLogAdmin"""
    list_display=('ip', 'type')


admin.site.register(DpoolLog, DpoolLogAdmin)