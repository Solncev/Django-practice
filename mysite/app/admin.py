from django.contrib import admin
from .models import UserProfile, Department, Type, AssignedKPI, KPI

admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(Type)
admin.site.register(AssignedKPI)
admin.site.register(KPI)
