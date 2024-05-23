from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home' ),
    path('login/', views.loginPage, name='login' ),
    path('logout/', views.logoutPage, name='logout' ),
    path('register/', views.register, name='register' ),
    path('search/', views.search, name='search'),
    path('category/', views.category, name='category'),
    path('detail/', views.detail, name='detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

