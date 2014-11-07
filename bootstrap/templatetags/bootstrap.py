from django import template
from django import forms
from django.template import loader
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def bootstrap_form(form, template=None):
    """
    Renders a Django form using Bootstrap markup. See http://getbootstrap.com/css/#forms
    for more information.

    The form rendering is controlled by the ``bootstrap/form.html``
    template, which renders any non-field errors as error alerts, followed by hidden fields,
    and finally visible fields, each rendered using the ``bootstrap_field`` templatetag.

    :param form: A Django form instance
    """

    templates = [
        'bootstrap/%s.html' % form.__class__.__name__.lower(),
        'bootstrap/form.html',
    ]
    if template:
        templates.insert(0, template)
    return loader.render_to_string(templates, {
        'form': form,
    })

@register.simple_tag
def bootstrap_field(field, classes='', template=None):
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
    templates = [
        'bootstrap/%s_%s.html' % (field.field.__class__.__name__.lower(), field.field.widget.__class__.__name__.lower()),
        'bootstrap/%s.html' % field.field.__class__.__name__.lower(),
        'bootstrap/field.html',
    ]
    if template:
        templates.insert(0, template)
    return loader.render_to_string(templates, {
        'field': field,
        'is_checkbox': isinstance(field.field.widget, forms.CheckboxInput),
        'extra_classes': classes,
    })

@register.simple_tag
def pager(total, page_size=10, page=1, param='page', querystring='', spread=7, template=None):
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
    templates = [
        'bootstrap/pager.html',
    ]
    if template:
        templates.insert(0, template)
    return loader.render_to_string(templates, {
        'page_range': page_range,
        'page': page,
        'param': param,
        'querystring': querystring,
    })

@register.simple_tag
def render_value(obj, field_name, template=None, classes='', label=None):
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
    try:
        # XXX: A little hacky having this here - it's defined in bioshare's PropertiesModel.
        label, value = obj.get_field(field_name)
    except:
        if label is None:
            label = field_name[0].upper() + field_name[1:].replace('_', ' ')
        value = getattr(obj, field_name, None)
        if hasattr(value, 'all'):
            value = list(value.all())
    return loader.render_to_string(templates, {
        'object': obj,
        'field': field_name,
        'label': label,
        'value': value,
        'extra_classes': classes,
    })
