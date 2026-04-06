from django import template

register = template.Library()

@register.filter(name='rupiah')
def rupiah(value):
    try:
        # Ubah ke integer, lalu format dengan separator ribuan (koma)
        # Lalu ganti koma menjadi titik sesuai standar Indonesia
        return "{:,}".format(int(value)).replace(',', '.')
    except (ValueError, TypeError):
        return value
