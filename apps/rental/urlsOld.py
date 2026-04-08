from django.urls import path
from . import views

app_name = 'rental'

urlpatterns = [
    # Tampilan depan (Afifah Kreatif)
    path('', views.landing_page, name='landing'),
    
    # Bagian Dashboard (Modular)
    path('dashboard/paket/', views.admin_paket_list, name='admin_paket_list'),
    path('dashboard/paket/add/', views.admin_paket_add, name='admin_paket_add'),
    path('dashboard/paket/edit/<int:pk>/', views.admin_paket_edit, name='admin_paket_edit'),
    path('dashboard/paket/delete/<int:pk>/', views.admin_paket_delete, name='admin_paket_delete'),

    path('dashboard/galeri/', views.admin_galeri_list, name='admin_galeri_list'),
    path('dashboard/galeri/add/', views.admin_galeri_add, name='admin_galeri_add'),
    path('dashboard/galeri/delete/<int:pk>/', views.admin_galeri_delete, name='admin_galeri_delete'),

    path('dashboard/hero/', views.admin_hero_list, name='admin_hero_list'),
    path('dashboard/hero/add/', views.admin_hero_add, name='admin_hero_add'),
    path('dashboard/hero/delete/<int:pk>/', views.admin_hero_delete, name='admin_hero_delete'),
]
