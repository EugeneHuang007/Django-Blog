#与前端相关
from django.conf.urls import url
from haystack.views import SearchView

from blog.views import index, archive, article, comment_post, do_logout, do_reg, do_login, category, tag,about,contact

urlpatterns = [
    url(r'^$',index , name = 'index'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^article/$', article, name='article'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
    url(r'^logout$', do_logout, name='logout'),
    url(r'^reg', do_reg, name='reg'),
    url(r'^login', do_login, name='login'),
    url(r'category/$',category,name='category'),
    url(r'tag/$', tag, name='tag'),
    url(r'about/$', about, name='about'),
    url(r'contact/$', contact, name='contact'),
    url(r'^search/$', SearchView(), name='haystack_search'),

]

