from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [

    path('activity-log/', views.activity_log, name='activity_log'),

    path('dashboard/', views.index, name='index'), # Halaman utama dashboard
    path('users/', views.user_list, name='user_list'), # Halaman list user
    path('users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/change-role/<int:user_id>/', views.change_role, name='change_role'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.site_settings, name='site_settings'),

    path('verify-reset/', views.verify_reset, name='verify_reset'),
    path('approve-reset/<int:request_id>/', views.approve_reset, name='approve_reset'),
]
