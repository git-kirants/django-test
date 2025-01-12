from django import template
register = template.Library()

@register.filter(name='addclass')
def addclass(field, css):
    return field.as_widget(attrs={"class": css}) 

@register.filter(name='addplaceholder')
def addplaceholder(field, placeholder):
    return field.as_widget(attrs={"placeholder": placeholder}) 