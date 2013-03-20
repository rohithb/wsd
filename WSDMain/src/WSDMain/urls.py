from django.conf.urls import patterns, url
from Editor.views import editor
from Parser.views import makeGraph, doWSD

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                      (r'^$',editor),
                      (r'^status/$',makeGraph),
                      (r'^doWSD/$',doWSD),
    # Examples:
    # url(r'^$', 'WSDMain.views.home', name='home'),
    # url(r'^WSDMain/', include('WSDMain.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
