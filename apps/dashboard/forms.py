from django import forms
from .models import SiteSetting

# apps/dashboard/forms.py
class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = ['site_name', 'active_theme']
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'active_theme': forms.Select(choices=[
                ('sb_admin', 'SB Admin 2 (Corporate)'),
                ('volt_dashboard', 'Volt Dashboard'), # <-- Sesuai kesepakatan
            ], attrs={'class': 'form-control'}),
        }
