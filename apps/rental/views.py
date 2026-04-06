from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.decorators import admin_only
from apps.dashboard.models import AuditLog # Tetap bisa akses model AuditLog
from .models import PaketSewa, Galeri, HeroSlider
from .forms import PaketSewaForm, GaleriForm, HeroSliderForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

def landing_page(request):
    # Ambil semua paket, urutkan dari yang termurah
    pakets = PaketSewa.objects.all().order_by('harga')
    return render(request, 'apps/rental/landing.html', {'pakets': pakets})

@login_required
@admin_only
def admin_paket_list(request):
    pakets = PaketSewa.objects.all().order_by('harga')
    # Perhatikan path template-nya, kita taruh di folder rental agar modular
    return render(request, 'apps/rental/dashboard/paket_list.html', {'pakets': pakets})

@login_required
@admin_only
def admin_paket_add(request):
    if request.method == 'POST':
        form = PaketSewaForm(request.POST)
        if form.is_valid():
            paket = form.save()
            AuditLog.objects.create(
                user=request.user, aksi='CREATE', tabel='PaketSewa',
                keterangan=f"Menambah paket sewa: {paket.nama}",
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"Paket {paket.nama} berhasil ditambahkan!")
            return redirect('rental:admin_paket_list') # Redirect ke namespace rental
    else:
        form = PaketSewaForm()
    
    return render(request, 'apps/rental/dashboard/paket_form.html', {
        'form': form, 
        'title': 'Tambah Paket Sewa'
    })

@login_required
@admin_only
def admin_paket_edit(request, pk):
    paket = get_object_or_404(PaketSewa, pk=pk)
    if request.method == 'POST':
        form = PaketSewaForm(request.POST, instance=paket)
        if form.is_valid():
            form.save()
            # Audit Log: UPDATE
            AuditLog.objects.create(
                user=request.user, aksi='UPDATE', tabel='PaketSewa',
                keterangan=f"Mengubah data paket: {paket.nama}",
                ip_address=get_client_ip(request)
            )
            messages.success(request, f"Paket {paket.nama} berhasil diperbarui!")
            return redirect('rental:admin_paket_list')
    else:
        form = PaketSewaForm(instance=paket)
    
    return render(request, 'apps/rental/dashboard/paket_form.html', {
        'form': form, 
        'title': f'Edit Paket: {paket.nama}'
    })

@login_required
@admin_only
def admin_paket_delete(request, pk):
    if request.method == 'POST':
        paket = get_object_or_404(PaketSewa, pk=pk)
        nama_paket = paket.nama
        paket.delete()
        
        # Audit Log: DELETE
        AuditLog.objects.create(
            user=request.user, aksi='DELETE', tabel='PaketSewa',
            keterangan=f"Menghapus paket: {nama_paket}",
            ip_address=get_client_ip(request)
        )
        messages.success(request, f"Paket {nama_paket} telah dihapus.")
    return redirect('rental:admin_paket_list')

@login_required
@admin_only
def admin_galeri_list(request):
    fotos = Galeri.objects.all().order_by('-created_at')
    return render(request, 'apps/rental/dashboard/galeri_list.html', {'fotos': fotos})

@login_required
@admin_only
def admin_galeri_add(request):
    if request.method == 'POST':
        # PENTING: Tambahkan request.FILES untuk menangani upload gambar
        form = GaleriForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save()
            AuditLog.objects.create(
                user=request.user, aksi='CREATE', tabel='Galeri',
                keterangan=f"Upload foto galeri: {foto.judul}",
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Foto berhasil diunggah!")
            return redirect('rental:admin_galeri_list')
    else:
        form = GaleriForm()
    return render(request, 'apps/rental/dashboard/galeri_form.html', {'form': form, 'title': 'Upload Foto Dokumentasi'})

@login_required
@admin_only
def admin_galeri_delete(request, pk):
    if request.method == 'POST':
        foto = get_object_or_404(Galeri, pk=pk)
        judul_foto = foto.judul
        
        # Opsi: Menghapus file fisik dari folder media (agar tidak nyampah di Linux Mint Anda)
        if foto.gambar:
            foto.gambar.delete()
            
        foto.delete()
        
        # Audit Log: DELETE
        AuditLog.objects.create(
            user=request.user, aksi='DELETE', tabel='Galeri',
            keterangan=f"Menghapus foto galeri: {judul_foto}",
            ip_address=get_client_ip(request)
        )
        messages.success(request, f"Foto '{judul_foto}' berhasil dihapus.")
    return redirect('rental:admin_galeri_list')

# Update fungsi landing_page untuk mengambil foto
def landing_page(request):
    slides = HeroSlider.objects.filter(is_active=True)
    pakets = PaketSewa.objects.all().order_by('harga')
    fotos = Galeri.objects.all().order_by('-created_at')[:6] # Ambil 6 foto terbaru

    return render(request, 'apps/rental/landing.html', {
        'slides': slides,
        'pakets': pakets, 
        'fotos': fotos
    })

@login_required
@admin_only
def admin_hero_list(request):
    slides = HeroSlider.objects.all().order_by('order')
    return render(request, 'apps/rental/dashboard/hero_list.html', {'slides': slides})

@login_required
@admin_only
def admin_hero_add(request):
    if request.method == 'POST':
        form = HeroSliderForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save()
            AuditLog.objects.create(
                user=request.user, aksi='CREATE', tabel='HeroSlider',
                keterangan=f"Menambah slide hero: {slide.judul_utama}",
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Slide hero berhasil ditambahkan!")
            return redirect('rental:admin_hero_list')
    else:
        form = HeroSliderForm()
    return render(request, 'apps/rental/dashboard/hero_form.html', {'form': form, 'title': 'Tambah Slide Hero'})

@login_required
@admin_only
def admin_hero_delete(request, pk):
    if request.method == 'POST':
        slide = get_object_or_404(HeroSlider, pk=pk)
        judul = slide.judul_utama
        slide.gambar_bg.delete()
        slide.delete()
        messages.success(request, f"Slide '{judul}' berhasil dihapus.")
    return redirect('rental:admin_hero_list')
