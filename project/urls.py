from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, profile, table, launch


urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/', include('djangosaml2.urls')),
    url(r'^$', index),
    url(r'^table/', table),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ht/$', include('health_check.urls')),
    url(r'^launch/', launch),

]
