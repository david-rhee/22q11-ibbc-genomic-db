# Core Django imports
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

# Third-party app imports

# Local app imports
from .views import About, Announcement, Contact, Home, Member_Site, Publication

urlpatterns = patterns('',
    # public area
    url(r'^$', '22q11-ibbc.views.Home', name='index'),
    url(r'^home/$', '22q11-ibbc.views.Home', name='home'),
    url(r'^about/$', '22q11-ibbc.views.About', name='about'),
    url(r'^annoucement/', '22q11-ibbc.views.Announcement', name='announcement'),
    url(r'^contact/', '22q11-ibbc.views.Contact', name='contact'),
    url(r'^member_site/$', '22q11-ibbc.views.Member_Site', name='member_site'),
    url(r'^publication/$', '22q11-ibbc.views.Publication', name='publication'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)