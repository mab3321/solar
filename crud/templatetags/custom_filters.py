from django import template

register = template.Library()

@register.filter(name='get_attr')
def get_attr(obj, attr_name):
    """ Retrieve attribute by name from an object. """
    res = getattr(obj, attr_name, "")
    if 'crud.models' in str(type(res)):
        name = getattr(res, 'name', "")
        brand = getattr(res, 'brand', "")
        if name:
            return name
        elif brand:
            return brand
        else:
            return ''
        
    else:
        return res
@register.filter
def is_queryset(item):
    if 'object' in str(item):
        return True
    else:
        return False
@register.filter
def is_invoice(model_instance):
    return model_instance.__class__.__name__ == 'Invoice'