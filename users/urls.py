from django.urls import path
from .views import DashboardView,EditProfileView,UsersListView,user_detail_view,FollowUserView


urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('edit/',EditProfileView.as_view(),name='edit_profile'),
    path('users/follow/',FollowUserView.as_view(),name='user_follow'),
    path('users/',UsersListView.as_view(),name='user_list'),
    path('users/<str:username>/',user_detail_view,name='user_detail'),
]