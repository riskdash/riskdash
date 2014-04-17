from django.contrib import admin
from apps.dashboard.models import SumStatistics
from apps.dashboard.models import CumRF
from apps.dashboard.models import GrangerCausalityConn

admin.site.register(SumStatistics)
admin.site.register(CumRF)
admin.site.register(GrangerCausalityConn)