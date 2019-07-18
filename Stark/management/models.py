from django.db import models

# Create your models here.

class Host(models.Model):
    hostname = models.CharField(max_length=128,unique=True)
    key = models.TextField()
    status_choices = ((0,'等待批准',),
                     (1,' 批准 '),
                     (2,' 拒绝'))
    os_type_choices = (
        ('redhat','Redhat/CentOS'),
        ('ubuntu','Ubuntu'),
        ('suse','Suse'),
        ('windows','Windows'),
    )

    os_type = models.CharField(choices=os_type_choices,max_length=128,default='redhat')
    status = models.SmallIntegerField(choices=status_choices,default=0,verbose_name="状态")

    def __str__(self):
        return self.hostname


class HostGroup(models.Model):
    name = models.CharField(max_length=64,unique=True)
    hosts = models.ManyToManyField(Host,blank=True)

    def __str__(self):
        return self.name

