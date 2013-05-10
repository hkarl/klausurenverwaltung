

from django.conf.urls import patterns, url
from django.conf import settings

from klausurensammlung import views

urlpatterns = patterns('',
                       url(r'^stufe', views.stufe.as_view(), name='stufe'),
                       url(r'^filtertab', views.filtertab.as_view(), name='filtertab'),
                       url(r'^schlagworte/stufe=(?P<stufe>[a-zA-Z\-0-9]+)/', views.schlagworte.as_view(), name='schlagworte'),
                       # url(r'klausur/(?P<stufe>[a-zA-Z\-0-9]+)/', views.klausur.as_view(), name='klausur'),
                       # url(r'klausur/', views.klausur.as_view(), name='klausur'),
                       url(r'^klausur/stufe=(?P<stufe>[a-zA-Z\-0-9]+)/sw=(?P<swIds>[^/]*)/stfragen=(?P<stids>[^/]*)/mcfragen=(?P<mcids>[^/]*)/', views.klausur.as_view(), name='klausur'),
                       url(r'^makePDF/st=(?P<stids>[^/]*)/mc=(?P<mcids>[^/]*)', views.makePDF.as_view(), name='makePDF'),
                       # url(r'^standardfrage/(\d{4})/$', views.standardfrage.as_view(), name='ks-standardfrage')
                       url(r'^standardfrage/(.*)/$', views.standardfrage.as_view(), name='standardfrage'),
                       url(r'^mcfrage/(.*)/$', views.mcfrage.as_view(), name='mcfrage'),
                       )
