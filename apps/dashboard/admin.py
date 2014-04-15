from django.contrib import admin
from apps.dashboard.models import SumStatistics
from apps.dashboard.models import CumRF

admin.site.register(SumStatistics)
admin.site.register(CumRF)