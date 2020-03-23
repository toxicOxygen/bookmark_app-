from django.urls import path
from .views import ImageCreateView,ImageDetailView,image_like,image_list

urlpatterns = [
    path('like/',image_like,name="image_like"),
    path('create/',ImageCreateView.as_view(),name='image_create'),
    path('<str:slug>/',ImageDetailView.as_view(),name='image_detail'),
    path('',image_list,name='list')
]