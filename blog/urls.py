from django.urls import path
from . import views
from .views import (PostsListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView)


urlpatterns = [
    path('success', views.success, name="success"),
    path('user_detail/', views.user_detail, name="user_detail"),
    path('posts/day/<int:day>', PostsListView.as_view(), name="artist-posts"),
    path('post/edit/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name="blog-about"),
    path('artist/<acount_id>', UserPostListView.as_view(), name="user-posts"),
]
