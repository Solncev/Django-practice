from django.contrib import admin
from .models import UserProfile, Department, AssignedKPI, KPI, Position, Comments, Budget, AcceptRejectKPI

admin.site.register(UserProfile)
admin.site.register(Department)
# <<<<<<< HEAD

# =======
admin.site.register(AssignedKPI)
admin.site.register(KPI)
admin.site.register(Position)
admin.site.register(Comments)
admin.site.register(Budget)
admin.site.register(AcceptRejectKPI)
# >>>>>>> 39f5a913329fc1904cd8450c52e8e358d86c0b65
# Register your models here.
