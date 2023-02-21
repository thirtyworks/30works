from django.urls import path
from . import views
from .views import (PostsListView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView)
from django.views.generic import RedirectView


urlpatterns = [
    path('success', views.success, name="success"),
    path('day/<int:day>', PostsListView.as_view(), name="artist-posts"),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/edit/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/edit/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name="about"),
    path('faq/', views.faq, name="faq"),
    path('profile/', views.profile),
    path('artist/<acount_id>', UserPostListView.as_view(), name="user-posts"),
]
