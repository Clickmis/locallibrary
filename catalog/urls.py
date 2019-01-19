from django.urls import path, re_path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$',
            views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors '),
    # path('', views.IndexView.as_view(), name='index'),
    # path('(?P<pk>[0-9]+)/', views.detail, name='detail'),
    # re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # re_path(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # re_path(r'^(?P<questionId>[0-9]+)/vote/$', views.vote, name='vote'),
]
