from django.urls import path
from . import views

# Tanpa app_name agar lebih mudah dipanggil secara global atau sesuaikan jika pakai namespace
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'), # Tambahkan ini
    path('reset-password-confirm/<uuid:token>/', views.reset_password_confirm, name='password_reset_confirm'),
]
