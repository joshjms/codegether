from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('projects/', views.project_list, name='list'),
    path('projects/<slug:slug>/', views.view_project, name='project'),
    path('create/', views.post_project, name='create'),
    path('upvote/<int:pid>', views.upvote, name='upvote'),

    path('user/<str:username>', views.profile, name='profile'),
    path('user/<str:username>/edit', views.profile_edit, name='profile_edit'),
]