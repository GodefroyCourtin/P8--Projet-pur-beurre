"""Contains the application’s url."""
from django.urls import path
from . import views
app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('<int:product_id>/', views.detail, name='detail'),
    path(
        'save/<int:product_id>/<int:product_id_replacement>/',
        views.save, name='save'),
    path('mentions_legal/', views.mentions_legal, name='mentions_legal'),
]
