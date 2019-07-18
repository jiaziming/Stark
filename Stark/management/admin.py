from django.contrib import admin

# Register your models here.
from management import models


admin.site.register(models.Host)
admin.site.register(models.HostGroup)