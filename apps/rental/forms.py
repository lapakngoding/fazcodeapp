from django import forms
from .models import PaketSewa, Galeri, HeroSlider, NamaWebsite, ListHarga

class NamaWebsiteForm(forms.ModelForm):
    class Meta:
        model = NamaWebsite
        fields = ['nama_web','address','google_maps_url','phone','email']
        widgets = {
            'nama_web': forms.TextInput(attrs={
                'class': 'form-control form-control-lg', 
                'placeholder': 'Contoh: Afifah Kreatif'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '0812-xxxx-xxxx'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'kontak@afifahkreatif.com'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Alamat Kantor'
            }),
            'google_maps_url': forms.TextInput(attrs={
                'class': 'form-control text-primary', 
                'placeholder': 'Paste link src iframe di sini...'
            }),
        }

class PaketSewaForm(forms.ModelForm):
    class Meta:
        model = PaketSewa
        fields = ['nama', 'harga', 'fitur', 'is_featured']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Paket Rumah'}),
            'harga': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1500000'}),
            'fitur': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tenda Dekorasi\n50 Kursi\nLampu'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'custom-control-input', 'id': 'customCheck1'}),
        }

class GaleriForm(forms.ModelForm):
    class Meta:
        model = Galeri
        fields = ['judul', 'gambar']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Misal: Dekorasi Pernikahan di GOR'}),
            'gambar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class HeroSliderForm(forms.ModelForm):
    class Meta:
        model = HeroSlider
        fields = ['logo','sub_judul', 'judul_utama', 'deskripsi', 'gambar_bg', 'order', 'is_active']
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'sub_judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Misal: Sejak 2010'}),
            'judul_utama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Afifah Kreatif'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gambar_bg': forms.FileInput(attrs={'class': 'form-control-file'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ListHargaForm(forms.ModelForm):
    class Meta:
        model = ListHarga
        fields = ['deskripsi', 'kategori', 'qty', 'satuan', 'per_hari', 'harga']
        widgets = {
            'deskripsi': forms.TextInput(attrs={'class': 'form-control'}),
            'kategori': forms.TextInput(attrs={'class': 'form-control'}),
            'qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'satuan': forms.Select(attrs={'class': 'form-control'}), # Jika pakai choices
            'harga': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExcelUploadForm(forms.Form):
    file_excel = forms.FileField(
        label="Pilih File Excel",
        help_text="Format file harus .xlsx atau .xls",
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
