from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out', views.sign_out, name='sign_out'),
    path('modif_password', views.modif_password, name='modif_password'),
    path('modif_email', views.modif_email, name='modif_email'),
    path('favorite',views.favorite, name='favorite'),
    path('remove_favorite/<int:product_id>/<int:product_id_replacement>/', views.remove_favorite, name='remove_favorite'),
    path('delete_account', views.delete_account, name='delete_account')
]