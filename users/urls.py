from users.models import Role
from django.urls import path 

from .views import (
    PermissionAPIView,
    ProfilePasswordAPIView,
    register, 
    login, 
    AuthenticatedUser, 
    logout, 
    RoleViewSet,
    UserGenericAPIView,
    profileInfoAPIView,
)

urlpatterns = [
    # path('users/', users),
    path('register/', register),
    path('login', login),
    path('logout', logout),
    path('user', AuthenticatedUser.as_view()),
    path('permissions', PermissionAPIView.as_view()),

    # Viewsets for role
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),



    path('users/info', profileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),



    # Gneric views
    path('users', UserGenericAPIView.as_view()),
    path('users/<str:pk>', UserGenericAPIView.as_view())
]