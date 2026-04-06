from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        # Pastikan pengecekan string 'ADMIN' sesuai dengan di Model
        if request.user.role == 'ADMIN' or request.user.role == 'SUPERADMIN':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Anda tidak memiliki izin akses ke halaman ini.")
            return redirect('dashboard:index') # Lempar ke halaman yang aman
    return wrapper_func
