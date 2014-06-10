from django import template
from django import forms
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.inclusion_tag('bootstrap/form.html')
def bootstrap_form(form):
    """
    Renders a Django form using Bootstrap markup. See http://getbootstrap.com/css/#forms
    for more information.

    The form rendering is controlled by the ``bootstrap/form.html``
    template, which renders any non-field errors as error alerts, followed by hidden fields,
    and finally visible fields, each rendered using the ``bootstrap_field`` templatetag.

    :param form: A Django form instance
    """
    return {
        'form': form,
    }

@register.inclusion_tag('bootstrap/field.html')
def bootstrap_field(field, classes=''):
    """
    Renders a bound Django field using Bootstrap markup. See http://getbootstrap.com/css/#forms
    for more information.

    The field rendering is specified in the ``bootstrap/field.html`` template, which will render
    ``form-group`` divs with ``has-error`` and ``required`` classes as appropriate, any field errors
    using Django's field error rendering (typically ``ul.errorlist``), and includes a ``help-block``
    element for help text when no errors are present.

    A special check is made for ``CheckboxInput`` widgets, so that the label appears after the
    input element instead of before.

    :param field: A BoundField instance, such as those returned by iterating over a form
    :param classes: Optional string of CSS classes to append to the ``<div class="form-group...">``
    """
    return {
        'field': field,
        'is_checkbox': isinstance(field.field.widget, forms.CheckboxInput),
        'extra_classes': classes,
    }

@register.inclusion_tag('bootstrap/pager.html')
def pager(total, page_size=10, page=1, param='page', querystring='', spread=7):
    """
    Renders a pager using Bootstrap's pagination markup, documented here:

        http://getbootstrap.com/components/#pagination

    The pager's template is ``bootstrap/pager.html``.

    :param total: The total number of results
    :param page_size: The page size
    :param page: The selected page number (1-based)
    :param param: The querystring parameter name for specifying a page
    :param querystring: The querystring of the current page. Can be gotten from ``request.GET.urlencode()``
    :param spread: The number of pages to show, with the current page in the center of the range
    """
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
def render_value(obj, field_name, template=None, classes=''):
    """
    Renders a static value as a ``p.form-control-static`` element wrapped in a ``div.form-group``,
    as suggested by http://getbootstrap.com/css/#forms-controls-static

    The template used to render the value depends on the ContentType of the object. The following
    templates are searched in order:

        * ``<app_label>/values/<model>_<field_name>.html``
        * ``<app_label>/values/<model>.html``
        * ``<app_label>/value.html``
        * ``bootstrap/value.html``
    """
    ct = ContentType.objects.get_for_model(obj)
    templates = [
        '%s/values/%s_%s.html' % (ct.app_label, ct.model, field_name),
        '%s/values/%s.html' % (ct.app_label, ct.model),
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
        'extra_classes': classes,
    })
