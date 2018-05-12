from django.contrib import admin
from . import models as ms

admin.site.register(ms.Museum)
admin.site.register(ms.Comment)
admin.site.register(ms.Added_Museum)
admin.site.register(ms.Collection)
