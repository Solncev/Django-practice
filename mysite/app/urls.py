from django.conf.urls import url
from django.templatetags.static import static

from app import views
from mysite import settings

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^main/', views.main, name='main'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^personal_information/', views.personal_information, name='personal_information'),

    # GET запрос через url

    url(r'^assign_kpi/(?P<id_department>\d+)/$', views.assign_kpi, name='assign_kpi'),
    url(r'^kpi/(?P<id_assigned_kpi>\d+)/$', views.kpi, name='kpi'),
    url(r'^kpi/(?P<flag>(accept|reject))/(?P<id_assigned_kpi>\d+)/$', views.accept, name='accept'),
    url(r'^kpi/report/(?P<id_assigned_kpi>\d+)/$', views.report, name='report'),

]