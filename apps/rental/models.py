from django.db import models

class PaketSewa(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=12, decimal_places=0) # Misal: 1500000
    fitur = models.TextField(help_text="Pisahkan fitur dengan koma (,) atau baris baru")
    is_featured = models.BooleanField(default=False) # Untuk label "Best Seller"
    
    def get_fitur_list(self):
        return [f.strip() for f in self.fitur.splitlines() if f.strip()]

class Galeri(models.Model):
    judul = models.CharField(max_length=100)
    gambar = models.ImageField(upload_to='galeri/') # Akan tersimpan di media/galeri/
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

class HeroSlider(models.Model):
    logo = models.ImageField(upload_to='hero/', help_text="Ukuran rekomendasi 1:1")
    sub_judul = models.CharField(max_length=200, help_text="Teks kecil di atas judul utama")
    judul_utama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    gambar_bg = models.ImageField(upload_to='hero/', help_text="Ukuran rekomendasi 1920x1080")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Urutan tampil")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.judul_utama
