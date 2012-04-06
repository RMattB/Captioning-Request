from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'captioning_request02.views.home', name='home'),
    # url(r'^captioning_request02/', include('captioning_request02.foo.urls')),
    # to do: simplify/shorten these URLs
    url(r'^captioning-request/$', 'captioning_request.views.index'),
    url(r'^captioning-request/my-requests/$', 'captioning_request.views.my_requests'),
    url(r'^captioning-request/(?P<captioning_request_id>\d+)/$', 'captioning_request.views.detail'),
    # to do: add these views
    # url(r'^captioning_request/(?P<request_id>\d+)/receive_captions/$', 'captioning_request.views.receive_captions', name='receive_captions'),
    # url(r'^captioning_request/(?P<request_id>\d+)/approve_captions/$', 'captioning_request.views.approve_captions', name='approve_captions'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'captioning-request/login.html'}),
)
urlpatterns += staticfiles_urlpatterns()
