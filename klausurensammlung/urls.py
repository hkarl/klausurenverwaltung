

from django.conf.urls import patterns, url
from django.conf import settings

from klausurensammlung import views

urlpatterns = patterns('',
                       url(r'^stufe', views.stufe.as_view(), name='stufe'),
                       url(r'^schlagworte/stufe=(?P<stufe>[a-zA-Z\-0-9]+)/', views.schlagworte.as_view(), name='schlagworte'),
                       # url(r'klausur/(?P<stufe>[a-zA-Z\-0-9]+)/', views.klausur.as_view(), name='klausur'),
                       # url(r'klausur/', views.klausur.as_view(), name='klausur'),
                       url(r'^klausur/stufe=(?P<stufe>[a-zA-Z\-0-9]+)/sw=(?P<swIds>[^/]*)/stfragen=(?P<stids>[^/]*)/mcfragen=(?P<mcids>[^/]*)/', views.klausur.as_view(), name='klausur'),
                       url(r'^makePDF/st=(?P<stids>[^/]*)/mc=(?P<mcids>[^/]*)', views.makePDF.as_view(), name='makePDF'),
                       )
