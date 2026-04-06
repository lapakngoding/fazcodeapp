from .models import SiteSetting

def theme_settings(request):
    config = SiteSetting.objects.first()
    return {
        'ACTIVE_THEME': f'themes/{config.active_theme}/' if config else 'themes/sb_admin/',
        'APP_NAME': config.site_name if config else 'Fazcodeapp'
    }
