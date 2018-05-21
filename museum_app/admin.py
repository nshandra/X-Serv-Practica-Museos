from django.contrib import admin
from . import models as ms
from django.contrib.sessions.models import Session

admin.site.register(ms.Museum)
admin.site.register(ms.Comment)
admin.site.register(ms.Added_Museum)
admin.site.register(ms.Collection)
admin.site.register(Session)