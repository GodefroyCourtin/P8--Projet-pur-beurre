"""Contains the application’s url."""
from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('', views.my_account, name='my_account'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('favorite', views.favorite, name='favorite'),
    path(
        'remove_favorite/<int:product_id>/<int:product_id_replacement>/',
        views.remove_favorite,
        name='remove_favorite'
        )
    ]
