from django.db import models

# Create your models here.

class rt(models.Model):
    rt_id = models.IntegerField()
    rt_title = models.CharField(max_length=256)
    rt_content = models.TextField()
    rt_status = models.CharField(max_length=64)
    rt_lock = models.BooleanField(default=False)
    product_name = models.ForeignKey('product')
    
    def __unicode__(self):
        return self.rt_title

class product(models.Model):
    #product name
    name = models.CharField(max_length=64,unique=True)
    #product line
    pline = models.CharField(max_length=64)
    #svn path
    svn_path = models.CharField(max_length=256)
    #rsync path
    rsync_path = models.CharField(max_length=256)
    #rsync port
    port = models.IntegerField()
    #rsync model
    model = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name
