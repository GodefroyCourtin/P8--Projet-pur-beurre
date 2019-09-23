from django.urls import path
from . import views
app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('substitute/<int:product_id>/', views.substitute, name='substitute'),
]