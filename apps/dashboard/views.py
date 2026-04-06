from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import admin_only
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import SiteSettingForm
from .models import SiteSetting, AuditLog
from apps.accounts.forms import UserCreateForm, UserUpdateForm, ProfileUpdateForm
from apps.accounts.models import PasswordResetRequest
from django.core.mail import send_mail
from django.utils import timezone


User = get_user_model()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
@admin_only
def index(request):
    context = {
        'total_user': User.objects.count(),
        'user_aktif': User.objects.filter(is_active=True).count(),
        'pending_reset': PasswordResetRequest.objects.filter(is_processed=False).count(),
        'recent_logs': AuditLog.objects.all()[:5], # Ambil 5 log terakhir untuk ringkasan
    }
    return render(request, 'apps/dashboard/index.html', context)

@login_required
@admin_only
def user_list(request):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak! Anda bukan Superadmin.")
        return redirect('dashboard:index')

    # Tambahkan baris print ini
    print("DEBUG: Menjalankan View user_list") 
    users = User.objects.all().order_by('-date_joined') #('-id')
    return render(request, 'apps/dashboard/user_list.html', {'users': users})

@login_required
def toggle_user_status(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard:index')

    target_user = get_object_or_404(User, id=user_id)
    if target_user != request.user:
        target_user.is_active = not target_user.is_active
        target_user.save()
        
        status_text = "Aktif" if target_user.is_active else "Nonaktif"
        AuditLog.objects.create(
            user=request.user,
            aksi='UPDATE',
            tabel='User',
            keterangan=f"Mengubah status user {target_user.username} menjadi {status_text}",
            ip_address=get_client_ip(request)
        )

        messages.success(request, f"Status {target_user.username} berhasil diubah.")
    else:
        messages.warning(request, "Anda tidak bisa menonaktifkan akun sendiri!")

    return redirect('dashboard:user_list')

@login_required
@admin_only
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user_baru = form.save() # Simpan ke variabel agar bisa ambil username-nya
            
            # --- AUDIT LOG: CREATE USER ---
            AuditLog.objects.create(
                user=request.user,
                aksi='CREATE',
                tabel='User',
                keterangan=f"Menambah user baru: {user_baru.username}",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, f"User {user_baru.username} berhasil ditambahkan!")
            return redirect('dashboard:user_list')
    else:
        form = UserCreateForm()
    return render(request, 'apps/dashboard/user_form.html', {'form': form, 'title': 'Tambah User'})

@login_required
@admin_only
def user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            
            # --- AUDIT LOG: UPDATE USER ---
            AuditLog.objects.create(
                user=request.user,
                aksi='UPDATE',
                tabel='User',
                keterangan=f"Mengupdate data user: {user_obj.username}",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, f"Data {user_obj.username} berhasil diperbarui!")
            return redirect('dashboard:user_list')
    else:
        form = UserUpdateForm(instance=user_obj)
    
    context = {
        'form': form,
        'user_obj': user_obj,
        'title': f'Edit User: {user_obj.username}'
    }
    return render(request, 'apps/dashboard/user_edit.html', context)

@login_required
@admin_only
def user_delete(request, user_id):
    if request.method == 'POST':
        user_to_delete = get_object_or_404(User, id=user_id)
        if user_to_delete == request.user:
            messages.error(request, "Anda tidak bisa menghapus akun Anda sendiri!")
        else:
            username = user_to_delete.username
            
            # --- AUDIT LOG: DELETE USER ---
            AuditLog.objects.create(
                user=request.user,
                aksi='DELETE',
                tabel='User',
                keterangan=f"Menghapus user: {username}",
                ip_address=get_client_ip(request)
            )
            
            user_to_delete.delete()
            messages.success(request, f"User {username} telah berhasil dihapus.")
    return redirect('dashboard:user_list')

@login_required
@admin_only
def change_role(request, user_id):
    if request.method == "POST":
        target_user = get_object_or_404(User, id=user_id)
        old_role = target_user.role # Simpan role lama untuk keterangan log
        new_role = request.POST.get('role')
        target_user.role = new_role
        target_user.save()
        
        # --- AUDIT LOG: CHANGE ROLE ---
        AuditLog.objects.create(
            user=request.user,
            aksi='UPDATE',
            tabel='User',
            keterangan=f"Mengubah role {target_user.username} dari {old_role} ke {new_role}",
            ip_address=get_client_ip(request)
        )
        
        messages.success(request, f"Role {target_user.username} berhasil diubah ke {new_role}!")
    return redirect('dashboard:user_list')


@login_required
@admin_only
def site_settings(request):
    config, created = SiteSetting.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = SiteSettingForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            
            # --- AUDIT LOG: SITE SETTINGS ---
            AuditLog.objects.create(
                user=request.user,
                aksi='UPDATE',
                tabel='SiteSetting',
                keterangan="Memperbarui pengaturan tampilan situs",
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, "Pengaturan tampilan berhasil diperbarui!")
            return redirect('dashboard:site_settings')
    else:
        form = SiteSettingForm(instance=config)
        
    return render(request, 'apps/dashboard/site_settings.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Cek form mana yang disubmit
        if 'update_profile' in request.POST:
            p_form = ProfileUpdateForm(request.POST, instance=request.user, user=request.user)
            pass_form = PasswordChangeForm(request.user)
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Profil Anda berhasil diperbarui!')
                return redirect('dashboard:profile')
        
        elif 'change_password' in request.POST:
            pass_form = PasswordChangeForm(request.user, request.POST)
            p_form = ProfileUpdateForm(instance=request.user, user=request.user)
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user) # Agar user tidak logout setelah ganti pass
                messages.success(request, 'Password Anda berhasil diubah!')
                return redirect('dashboard:profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user, user=request.user)
        pass_form = PasswordChangeForm(request.user)

    return render(request, 'apps/dashboard/profile.html', {
        'p_form': p_form,
        'pass_form': pass_form
    })

@login_required
def verify_reset(request):
    if not request.user.is_superuser:
        messages.error(request, "Anda tidak memiliki akses ke halaman verifikasi.")
        return redirect('dashboard:index')
        
    # GANTI order_of MENJADI order_by
    reset_requests = PasswordResetRequest.objects.filter(is_processed=False).order_by('-created_at')
    return render(request, 'apps/dashboard/verify_reset.html', {'reset_requests': reset_requests})

@login_required
@admin_only
def approve_reset(request, request_id):
    if not request.user.is_superuser:
        return redirect('dashboard:index')

    reset_req = get_object_or_404(PasswordResetRequest, id=request_id)
    reset_req.approved_at = timezone.now()
    reset_req.is_processed = True
    reset_req.save()

    AuditLog.objects.create(
        user=request.user,
        aksi='UPDATE',
        tabel='PasswordReset',
        keterangan=f"Menyetujui permintaan reset password untuk: {reset_req.user.username}",
        ip_address=get_client_ip(request)
    )

    # --- PERBAIKAN DI SINI ---
    # Jangan tulis manual /reset-password-..., biarkan reverse yang bekerja
    relative_url = reverse('password_reset_confirm', kwargs={'token': reset_req.token})
    reset_link = request.build_absolute_uri(relative_url)
    # -------------------------

    subject = "Link Reset Password Fazcodeapp"
    message = f"Halo {reset_req.user.username},\n\n" \
              f"Permintaan reset password Anda telah disetujui. " \
              f"Klik link di bawah (berlaku 1 jam):\n\n{reset_link}"
    
    # Cetak di terminal dengan pembatas agar tidak terpotong (Wrap) saat di-copy
    print("\n" + "="*50)
    print("KLIK RESET LINK DI BAWAH:")
    print(reset_link)
    print("="*50 + "\n")
    
    send_mail(subject, message, 'admin@fazcodeapp.com', [reset_req.user.email])
    
    messages.success(request, f"Permintaan {reset_req.user.username} disetujui.")
    return redirect('dashboard:verify_reset')

@login_required
def activity_log(request):
    if not request.user.is_superuser:
        return redirect('dashboard:index')
    
    logs = AuditLog.objects.all()[:100] # Ambil 100 aktivitas terbaru
    return render(request, 'apps/dashboard/activity_log.html', {'logs': logs})
