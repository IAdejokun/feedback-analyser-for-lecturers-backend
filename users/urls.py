from django.urls import path
from .views import *

urlpatterns = [
    # user urls
    path('register', RegisterUserView.as_view(), name = 'register'),
    path('login', LoginUserView.as_view(), name='login'),
    path('logout', LogoutUserView.as_view(), name='logout'),
    path('user/me', UserViewSet.as_view({'get': 'retrieve'}), name='user'),
    path('user/me/update', UpdateUserViewsSet.as_view({'patch': 'update'}), name='update_user'),
    
    # university urls
    path('universitylist', UniversityListView.as_view(), name='universities')
]