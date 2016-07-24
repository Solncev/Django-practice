from django.contrib import admin
from .models import UserProfile, Department, AssignedKPI, KPI, Position, Comments, Budget

admin.site.register(UserProfile)
admin.site.register(Department)
admin.site.register(AssignedKPI)
admin.site.register(KPI)
admin.site.register(Position)
admin.site.register(Comments)
admin.site.register(Budget)
