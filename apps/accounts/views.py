from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import PasswordResetRequest
from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index') # Jika sudah login, lempar ke dashboard

    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        
        user = authenticate(request, username=u_name, password=p_word)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Selamat datang kembali, {user.username}!")
            return redirect('dashboard:index')
        else:
            # Pesan inilah yang akan muncul di alert login.html Anda
            messages.error(request, "Username atau Password salah. Silakan coba lagi.")
            
    return render(request, 'apps/accounts/login.html') # Sesuaikan path template login Anda

def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah berhasil logout.")
    return redirect('login')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Buat request baru
            PasswordResetRequest.objects.create(user=user)
            messages.success(request, "Permintaan reset telah dikirim. Silakan hubungi Superadmin untuk verifikasi.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Email tidak terdaftar di sistem kami.")
    
    return render(request, 'apps/accounts/forgot_password.html')

# Di apps/accounts/views.py
def reset_password_confirm(request, token):
    # 1. Cari request berdasarkan token UUID
    reset_req = get_object_or_404(PasswordResetRequest, token=token)
    
    # 2. Cek Validasi (Apakah sudah diapprove dan belum expired 1 jam)
    if not reset_req.is_valid():
        messages.error(request, "Link reset sudah kadaluwarsa atau belum disetujui.")
        return redirect('login')

    if request.method == 'POST':
        new_pass = request.POST.get('password')
        conf_pass = request.POST.get('confirm_password')
        
        if new_pass == conf_pass:
            # 3. Update Password User
            user = reset_req.user
            user.set_password(new_pass)
            user.save()
            
            # 4. Hapus request agar token tidak bisa dipakai lagi (Keamanan)
            reset_req.delete()
            
            messages.success(request, "Password berhasil diperbarui! Silakan login.")
            return redirect('login')
        else:
            messages.error(request, "Konfirmasi password tidak cocok.")

    return render(request, 'apps/accounts/reset_confirm.html')
