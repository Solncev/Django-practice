from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^main/', views.main, name='main'),
    url(r'^logout/', views.logout, name='logout'),
    # GET запрос через url
    url(r'^assign_kpi/(?P<id_department>\d+)/$', views.assign_kpi, name='assign_kpi')
]