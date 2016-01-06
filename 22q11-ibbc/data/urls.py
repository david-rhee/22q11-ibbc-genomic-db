# Core Django imports
from django.conf.urls import patterns, include, url

# Third-party app imports

# Local app imports
from .views import home
from .views import site_detail_view, affymetrix_folder_download
from .views import UserProfile_DetailView
from .views import Subject_all_ListView, subject_search_view, Subject_search_ListView, Subject_site_ListView, Subject_DetailView
from .views import Affymetrix_all_ListView, affymetrix_search_view, Affymetrix_search_ListView, Affymetrix_site_ListView, Affymetrix_DetailView, affymetrix_download
from .views import wgs, wgs_download
from .views import Documents_1, Documents_2, Documents_3, Documents_4, Documents_5
from .views import logout_view

urlpatterns = patterns('',
    # Home
    url(r'^$', 'data.views.home', name='home'),

    # Site
    url(r'^site/(?P<pk>\d+)/$', site_detail_view, name='site_detail'),
    url(r'^site/download/(\S+)/$', affymetrix_folder_download , name='affymetrix_folder_download'),

    # UserProfile
    url(r'^user-profile/(?P<pk>\d+)/$', UserProfile_DetailView.as_view(), name='user_profile_detail'),

    # Subject
    url(r'^subject/list/$', Subject_all_ListView.as_view(), name='subject_all_list'),
    url(r'^subject/list/search/$', subject_search_view, name='subject_search'),
    url(r'^subject/list/(?P<g>[\w ]+)/(?P<l>[\w ]+)/(?P<a>[\w ]+)/(?P<s>[\w ]+)/$', Subject_search_ListView.as_view(), name='subject_search_list'),
    url(r'^subject/list/(?P<pk>\d+)/$', Subject_site_ListView.as_view(), name='subject_site_list'),
    url(r'^subject/(?P<pk>\d+)/$', Subject_DetailView.as_view(), name='subject_detail'),

    # Affymetrix
    url(r'^affymetrix/list/$', Affymetrix_all_ListView.as_view(), name='affymetrix_all_list'),
    url(r'^affymetrix/list/search/$', affymetrix_search_view, name='affymetrix_search'),
    url(r'^affymetrix/list/(?P<a>[\w ]+)/$', Affymetrix_search_ListView.as_view(), name='affymetrix_search_list'),
    url(r'^affymetrix/list/(?P<pk>\d+)/$', Affymetrix_site_ListView.as_view(), name='affymetrix_site_list'),
    url(r'^affymetrix/(?P<pk>\d+)/$', Affymetrix_DetailView.as_view(), name='affymetrix_detail'),
    url(r'^affymetrix/(?P<pk>\d+)/download/$', affymetrix_download , name='affymetrix_download'),

    # WGS
    url(r'^wgs/$', 'data.views.wgs', name='wgs'),
    url(r'^wgs/download/(\S+)/$', wgs_download , name='wgs_download'),

    # Documents
    url(r'^documents_1/$', 'data.views.Documents_1', name='documents_1'),
    url(r'^documents_2/$', 'data.views.Documents_2', name='documents_2'),
    url(r'^documents_3/$', 'data.views.Documents_3', name='documents_3'),
    url(r'^documents_4/$', 'data.views.Documents_4', name='documents_4'),
    url(r'^documents_5/$', 'data.views.Documents_5', name='documents_5'),

    # log on/off
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'data/data_login.html'}, name='22q11_ibbc_login'),
    url(r'^logout/$', logout_view, name='22q11_ibbc_logout'),
)