from django import template
from django import forms
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.inclusion_tag('bootstrap/form.html')
def bootstrap_form(form):
    return {
        'form': form,
    }

@register.inclusion_tag('bootstrap/field.html')
def bootstrap_field(field):
    return {
        'field': field,
        'is_checkbox': isinstance(field.field.widget, forms.CheckboxInput),
    }

@register.inclusion_tag('bootstrap/pager.html')
def pager(total, page_size=10, page=1, param='page', querystring='', spread=7):
    paginator = Paginator(range(total), page_size)
    page = paginator.page(page)
    if paginator.num_pages > spread:
        start = max(1, page.number - (spread // 2))
        page_range = range(start, start + spread)
    else:
        page_range = paginator.page_range
    return {
        'page_range': page_range,
        'page': page,
        'param': param,
        'querystring': querystring,
    }

@register.simple_tag
def render_value(obj, field_name, template=None):
    ct = ContentType.objects.get_for_model(obj)
    templates = [
        '%s/values/%s_%s.html' % (ct.app_label, ct.model, field_name),
        '%s/value.html' % ct.app_label,
        'bootstrap/value.html',
    ]
    if template:
        templates.insert(0, template)
    label, value = obj.get_field(field_name)
    return loader.render_to_string(templates, {
        'object': obj,
        'field': field_name,
        'label': label,
        'value': value,
    })
