from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('listings/', views.listings, name='listings'),
    path('detail/<album_id>/', views.detail, name='detail'),
    path('search/', views.search, name='search')
]