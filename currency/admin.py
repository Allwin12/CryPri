from django.contrib import admin
from .models import crontab,Table,Price, Marketdata, converter, MainTable

admin.site.register(crontab)
admin.site.register(converter)
admin.site.register(Table)
admin.site.register(Price)
admin.site.register(Marketdata)
admin.site.register(MainTable)