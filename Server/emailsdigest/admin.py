from django.contrib import admin
from emailsdigest import models

admin.site.register(models.Application)
admin.site.register(models.Email)
