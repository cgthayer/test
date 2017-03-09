from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

from views import (
    like_list_ajax, like_get_ajax,
    like_save_ajax, like_clear_ajax,
    bookmark_list_ajax, bookmark_get_ajax,
    bookmark_save_ajax, bookmark_clear_ajax,
)

# app_name = 'userlinks'

urlpatterns = [
    url(r'ajax/like_list/$',
        like_list_ajax, name='like_list_ajax'),
    url(r'ajax/like_get/(?P<target_type>[^/]+)/(?P<target_id>[^/]+)$',
        like_get_ajax, name='like_get_ajax'),
    url(r'ajax/like_get/$',
        like_get_ajax, name='like_get_ajax'),

    url(r'ajax/like_save/(?P<target_type>[^/]+)/(?P<target_id>[^/]+)$',
        like_save_ajax, name='like_save_ajax'),
    url(r'ajax/like_save/$',
        like_save_ajax, name='like_save_ajax'),
    url(r'ajax/like_clear/(?P<target_type>[^/]+)/(?P<target_id>[^/]+)$',
        like_clear_ajax, name='like_clear_ajax'),
    url(r'ajax/like_clear/$',
        like_clear_ajax, name='like_clear_ajax'),

    url(r'ajax/bookmark_list/$',
        bookmark_list_ajax, name='bookmark_list_ajax'),
    url(r'ajax/bookmark_get/(?P<target_type>[^/]+)/(?P<target_id>[0-9]+)$',
        bookmark_get_ajax, name='bookmark_get_ajax'),
    url(r'ajax/bookmark_get/$',
        bookmark_get_ajax, name='bookmark_get_ajax'),

    url(r'ajax/bookmark_save/(?P<target_type>[^/]+)/(?P<target_id>[0-9]+)$',
        bookmark_save_ajax, name='bookmark_save_ajax'),
    url(r'ajax/bookmark_save/$',
        bookmark_save_ajax, name='bookmark_save_ajax'),
    url(r'ajax/boomark_clear/(?P<target_type>[^/]+)/(?P<target_id>[0-9]+)$',
        bookmark_clear_ajax, name='bookmark_clear_ajax'),
    url(r'ajax/boomark_clear$',
        bookmark_clear_ajax, name='bookmark_clear_ajax'),
]

