from django.urls import path
from . import views

urlpatterns = [
    path('mypage/update_profile', views.update_profile, name='update_profile'),
    path('mypage', views.mypage, name='mypage'),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    path(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    path(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    path('post2', views.post_list2, name='post_list2'),
    path('post2/<int:pk>/', views.post_detail2, name='post_detail2'),
    path('post2/new/', views.post_new2, name='post_new2'),
    path('post2/<int:pk>/edit/', views.post_edit2, name='post_edit2'),
    path('post2/<pk>/remove/', views.post_remove2, name='post_remove2'),
    path(r'^post2/(?P<pk>\d+)/comment/$', views.add_comment_to_post2, name='add_comment_to_post2'),
    path(r'^comment2/(?P<pk>\d+)/approve/$', views.comment_approve2, name='comment_approve2'),
    path(r'^comment2/(?P<pk>\d+)/remove/$', views.comment_remove2, name='comment_remove2'),
    path(r'accounts/signup/', views.signup, name='signup'),
]