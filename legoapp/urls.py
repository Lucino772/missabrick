from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('download/<str:set_number>', views.download_set, name='download'),
    path('report', views.report, name='report')
]