from django.conf.urls import include, url
from django.contrib import admin
import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'rnaseq_webapp_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^analysis/', include('analysis.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls'))
]
