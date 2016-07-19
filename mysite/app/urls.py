from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^logout/', views.logout, name='logout'),
]