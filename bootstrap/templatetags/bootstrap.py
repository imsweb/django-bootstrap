from django import forms, template
from django.conf import settings
from django.core.paginator import Paginator
from django.template import loader
from django.utils import dateformat
from django.utils.encoding import force_str
from django.utils import formats
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import datetime
import os

register = template.Library()

# https://fortawesome.github.io/Font-Awesome/icons/#file-type
FONT_AWESOME_FILE_TYPE_ICON_MAP = {
    'doc': 'fa-file-word-o',
    'docx': 'fa-file-word-o',
    'pdf': 'fa-file-pdf-o',
    'pps': 'fa-file-powerpoint-o',
    'ppsx': 'fa-file-powerpoint-o',
    'ppt': 'fa-file-powerpoint-o',
    'pptx': 'fa-file-powerpoint-o',
    'rtf': 'fa-file-text-o',
    'txt': 'fa-file-text-o',
    'xls': 'fa-file-excel-o',
    'xlsx': 'fa-file-excel-o',
    'zip': 'fa-file-archive-o',
}


@register.simple_tag
def bootstrap_form(form, template=None, **kwargs):
    """
    Renders a Django form using Bootstrap markup. See https://getbootstrap.com/docs/5.1/forms/overview/
    for more information.

    By default, the form rendering is controlled by the ``bootstrap/form.html``
    template, which renders any non-field errors as error alerts, followed by hidden fields,
    and finally visible fields, each rendered using the ``bootstrap_field`` templatetag.

    This tag will also search for ``bootstrap/<form_class>.html`` first, if it exists. For a
    form class named RequestForm, ``bootstrap/requestform.html`` will be checked.

    :param form: A Django form instance
    """
    templates = [
        'bootstrap/%s.html' % form.__class__.__name__.lower(),
        'bootstrap/form.html',
    ]
    if template:
        templates.insert(0, template)
    params = {'form': form}
    params.update(kwargs)
    return loader.render_to_string(templates, params)


@register.simple_tag
def bootstrap_field(field, classes='', template=None, **kwargs):
    """
    Renders a bound Django field using Bootstrap markup. See http://getbootstrap.com/css/#forms
    for more information.

    By default, the field rendering is specified in the ``bootstrap/field.html`` template, which will render
    ``mb-3`` divs with ``form-check`` and ``required`` classes as appropriate, any field errors
    using Django's field error rendering (typically ``ul.errorlist``) along with Bootstrap 5's
    ``invalid-feedback`` class, and includes a ``form-text text-muted`` element for help text.

    A special check is made for ``CheckboxInput`` widgets, so that the label appears after the
    input element instead of before.

    This tag will also first search for the specified ``template`` (if provided), then for templates named
    ``bootstrap/<field_class>_<widget_class>.html`` or ``bootstrap/<field_class>.html`` before falling back
    to ``bootstrap/field.html``. For instance, a CharField with a Textarea widget will first look for
    ``bootstrap/charfield_textarea.html``, then ``bootstrap/charfield.html``.

    :param field: A BoundField instance, such as those returned by iterating over a form
    :param classes: Optional string of CSS classes to append to the ``<div class="mb-3...">``
    """
    if not field:
        return ''
    field_class = field.field.__class__.__name__.lower()
    widget_class = field.field.widget.__class__.__name__.lower()
    templates = [
        'bootstrap/%s_%s.html' % (field.form.__class__.__name__.lower(), field.name),
        'bootstrap/%s_%s.html' % (field_class, widget_class),
        'bootstrap/%s.html' % field_class,
        'bootstrap/field.html',
    ]
    if template:
        templates.insert(0, template)
    extra_classes = getattr(field.field, 'css_classes', [])
    if extra_classes:
        classes += ' ' + ' '.join(extra_classes)

    use_fieldset = getattr(field.field.widget, 'use_fieldset', False)
    describedby = set(field.field.widget.attrs.get('aria-describedby', '').split())
    labelledby = set(field.field.widget.attrs.get('aria-labelledby', '').split())

    # Need to shoehorn some ARIA attributes onto the widget based on information
    # on the field
    if use_fieldset:
        describedby.add('%s-label' % field.auto_id)
    else:
        labelledby.add('%s-label' % field.auto_id)
        field.field.widget.attrs['aria-labelledby'] = ' '.join(labelledby)

    if field.help_text:
        describedby.add('%s-help' % field.auto_id)
    if field.errors:
        field.field.widget.attrs['class'] = field.field.widget.attrs.get('class', '') + ' is-invalid'
        describedby.add('%s-errors' % field.auto_id)

    if describedby:
        field.field.widget.attrs['aria-describedby'] = ' '.join(describedby)

    params = {
        'field': field,
        'is_checkbox': isinstance(field.field.widget, forms.CheckboxInput),
        'show_label': getattr(field.field.widget, 'show_label', True),
        'use_fieldset': use_fieldset,
        'field_class': field_class,
        'widget_class': widget_class,
        'extra_classes': classes.strip(),
    }
    params.update(kwargs)
    return loader.render_to_string(templates, params)


@register.simple_tag
def render_readonly(field, template=None, **kwargs):
    if not field or field.is_hidden:
        return ''
    field_class = field.field.__class__.__name__.lower()
    widget_class = field.field.widget.__class__.__name__.lower()
    templates = [
        'bootstrap/%s_%s_readonly.html' % (field.form.__class__.__name__.lower(), field.name),
        'bootstrap/%s_%s_readonly.html' % (field_class, widget_class),
        'bootstrap/%s_readonly.html' % field_class,
        'bootstrap/field_readonly.html',
    ]
    if template:
        templates.insert(0, template)
    value = field.field.to_python(field.value())
    if hasattr(field.field.widget, 'render_readonly'):
        rendered = field.field.widget.render_readonly(value)
    else:
        short_dates = kwargs.pop('short_dates', True)
        rendered = stringify(value, short_dates=short_dates)
    params = {
        'field': field,
        'value': value,
        'rendered_value': rendered,
        'field_class': field_class,
        'widget_class': widget_class,
    }
    params.update(kwargs)
    return loader.render_to_string(templates, params)


@register.simple_tag
def pager(total, page_size=10, page=1, param='page', querystring='', spread=7, template=None):
    """
    Renders a pager using Bootstrap's pagination markup, documented here:

        https://getbootstrap.com/docs/5.1/components/pagination/

    The pager's template is ``bootstrap/pager.html`` by default, unless ``template`` is specified.

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
def render_value(obj, field_name, template=None, classes='', label=None, default='', **kwargs):
    """
    Renders a static value as a ``p.form-control-plaintext`` element wrapped in a ``div.mb-3``.

    The template used to render the value depends on the ContentType of the object. The following
    templates are searched in order:

        * ``<app_label>/values/<model>_<field_name>.html``
        * ``<app_label>/values/<model>.html``
        * ``<app_label>/value.html``
        * ``bootstrap/value.html``
    """
    from django.contrib.contenttypes.models import ContentType
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
        _label, value = obj.get_field(field_name)
        if label is None:
            label = _label
    except:
        if label is None:
            label = field_name[0].upper() + field_name[1:].replace('_', ' ')
        value = getattr(obj, field_name, None)
        if hasattr(value, 'all'):
            value = list(value.all())
    params = {
        'object': obj,
        'field': field_name,
        'label': label,
        'value': value,
        'extra_classes': classes,
        'default_value': default,
    }
    params.update(kwargs)
    return loader.render_to_string(templates, params)


@register.simple_tag
def stringify(value, sep=', ', default='', linebreaks=True, escape_html=True, short_dates=False):
    if value is None:
        value = default
    elif isinstance(value, bool):
        value = _('Yes') if value else _('No')
    elif isinstance(value, (list, tuple)):
        value = sep.join(stringify(v) for v in value)
    elif isinstance(value, dict):
        parts = []
        for key, value in value.items():
            if key and value:
                parts.append('%s: %s' % (key, stringify(value)))
        value = sep.join(parts)
    elif isinstance(value, datetime.datetime):
        value = formats.date_format(value, 'SHORT_DATETIME_FORMAT' if short_dates else 'DATETIME_FORMAT')
    elif isinstance(value, datetime.date):
        value = formats.date_format(value, 'SHORT_DATE_FORMAT' if short_dates else 'DATE_FORMAT')
    # The default value should be used if the string representation is empty, not just the value itself.
    value = force_str(value) or default
    if escape_html:
        value = escape(value)
    if linebreaks:
        value = value.replace('\r\n', '\n').replace('\n', '<br />')
    return mark_safe(value)


@register.filter
def file_extension_icon(ext, default='fa-file-o'):
    return FONT_AWESOME_FILE_TYPE_ICON_MAP.get(ext.lstrip('.').lower(), default)


@register.filter
def filename_icon(filename, default='fa-file-o'):
    _root, ext = os.path.splitext(filename)
    return file_extension_icon(ext, default=default)
