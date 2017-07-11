from django.conf.urls import include, url
from django.contrib import admin

from soc.views import index, table, departments


urlpatterns = [
    url(r'^accounts/', include('djangosaml2.urls')),
    url(r'^$', index),
    url(r'^table/', table),
    url(r'^dept_grps/$', departments)
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ht/$', include('health_check.urls')),
]
