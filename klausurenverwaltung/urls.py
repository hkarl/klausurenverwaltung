from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

    url(r'^$', 'klausurenverwaltung.views.home', name='home'),
    # url(r'^klausurenverwaltung/', include('klausurenverwaltung.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # pull in the klausurverwaltungs app:
    url (r'^klausurensammlung/', include ('klausurensammlung.urls')),
)
