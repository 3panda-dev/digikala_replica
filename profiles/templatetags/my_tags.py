from django import template 


register = template.Library()

@register.filter(name='phone_format')
def phone_format(phone, delimiter='-'):
    if len(phone) != 11 or not phone.isdigit():
        return phone
    return f'{phone[:4]}{delimiter}{phone[4:7]}{delimiter}{phone[7:]}'