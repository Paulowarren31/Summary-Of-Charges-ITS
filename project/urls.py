from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from soc.views import index, table, departments, dept_info, download, search


urlpatterns = [
    url(r'^accounts/', include('djangosaml2.urls')),
    url(r'^$', index),
    url(r'^dept_id', dept_info),
    url(r'^table/', table),
    url(r'^search/', search),
    url(r'^download/', download),
    url(r'^dept_grps/$', departments),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ht/$', include('health_check.urls')),
]

if settings.DEBUG:
  import debug_toolbar
  urlpatterns = [
    url(r'^debug/', include(debug_toolbar.urls)),
  ] + urlpatterns
