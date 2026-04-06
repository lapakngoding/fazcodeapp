from django import forms
from .models import PaketSewa, Galeri, HeroSlider

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
        fields = ['sub_judul', 'judul_utama', 'deskripsi', 'gambar_bg', 'order', 'is_active']
        widgets = {
            'sub_judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Misal: Sejak 2010'}),
            'judul_utama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Afifah Kreatif'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gambar_bg': forms.FileInput(attrs={'class': 'form-control-file'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
