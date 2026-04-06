from django.db import models
from django.conf import settings

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="Fazcodeapp")
    active_theme = models.CharField(max_length=50, default="sb_admin")

    class Meta:
        app_label = 'dashboard' # Menegaskan ini milik app dashboard
    
    def __str__(self):
        return self.site_name

class AuditLog(models.Model):
    AKSI_CHOICES = [
        ('CREATE', 'Tambah Data'),
        ('UPDATE', 'Ubah Data'),
        ('DELETE', 'Hapus Data'),
        ('LOGIN', 'Login'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    aksi = models.CharField(max_length=10, choices=AKSI_CHOICES)
    tabel = models.CharField(max_length=50) # Misal: 'Mahasiswa' atau 'User'
    keterangan = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.aksi} - {self.tabel}"
