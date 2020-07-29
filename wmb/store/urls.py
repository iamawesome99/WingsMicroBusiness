from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:branch>', views.branch_detail, name='branch_detail'),
    path('<str:branch>/products', views.branch_products, name='branch_products'),
    path('<str:branch>/products/<int:product_id>', views.product_detail, name='product_detail'),
    path('<str:branch>/products/<int:product_id>/buy', views.buy, name='buy'),
    path('<str:branch>/cart', views.cart, name='cart'),
    path('<str:branch>/cart/remove/<int:number>', views.remove_cart, name='remove_from_cart'),
    path('<str:branch>/cart/remove/all', views.clear_cart, name='clear_cart'),
    path('<str:branch>/cart/change/', views.change_cart, name='change_cart'),
    path('<str:branch>/search', views.search, name='search'),
]
