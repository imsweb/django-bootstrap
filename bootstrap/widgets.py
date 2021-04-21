from django import forms
from django.forms.utils import flatatt
from django.template import loader
from django.utils.translation import ugettext_lazy as _

import collections


class TemplateWidget (forms.Widget):
    """
    A widget that renders the specified ``template_name`` with the following context
    (plus any ``extra_context``):

        name
            The name of the field
        value
            The field's current value
        attrs
            Flattened HTML attributes
        widget
            A reference to ``self``
    """

    template_name = None
    extra_context = {}

    def __init__(self, template_name=None, attrs=None, **extra_context):
        if template_name:
            self.template_name = template_name
        self.extra_context.update(extra_context)
        super(TemplateWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        template = loader.get_template(self.template_name)
        # Don't use build_attrs, since the signature changed between 1.10 and 1.11.
        final_attrs = dict(self.attrs, name=name)
        if attrs:
            final_attrs.update(attrs)
        params = {
            'name': name,
            'value': value,
            'attrs': flatatt(final_attrs),
            'widget': self,
        }
        params.update(self.extra_context)
        return template.render(params)


class BootstrapWidget (object):
    """
    Base class for most widgets implemented here (with the exception of :class:`TemplateWidget`).
    """

    css_classes = ('form-control',)
    """
    A tuple of CSS classes to apply to the rendered widget, in addition to any ``class`` attribute specified.
    """

    extra_attrs = {}
    """
    Extra input attributes, defined on a class level.
    """

    def build_attrs(self, *args, **kwargs):
        attrs = super(BootstrapWidget, self).build_attrs(*args, **kwargs)
        if self.is_required and not isinstance(self, RadioSelect):
            attrs.update({'aria-required': 'true'})
        if self.is_required and isinstance(self, RadioSelect):
            attrs.update({'required': 'required'})
        attrs.update(self.extra_attrs)
        new_class = '%s %s' % (attrs.get('class', ''), ' '.join(self.css_classes))
        attrs['class'] = new_class.strip()
        return attrs


class TextInput (BootstrapWidget, forms.TextInput):
    """ Bootstrap version of ``forms.TextInput`` """


class AutofocusTextInput (TextInput):
    """ Autofocusing TextInput widget. """
    extra_attrs = {'autofocus': 'autofocus'}


class PasswordInput (BootstrapWidget, forms.PasswordInput):
    """ Bootstrap version of ``forms.PasswordInput`` """


class AutofocusPasswordInput (PasswordInput):
    """ Autofocusing PasswordInput widget. """
    extra_attrs = {'autofocus': 'autofocus'}


class Textarea (BootstrapWidget, forms.Textarea):
    """ Bootstrap version of ``forms.Textarea`` """


class AutofocusTextarea (Textarea):
    """ Autofocusing Textarea widget. """
    extra_attrs = {'autofocus': 'autofocus'}


class DateInput (BootstrapWidget, forms.DateInput):
    """ Bootstrap version of ``forms.DateInput``. The input is rendered with an extra "date" class. """
    css_classes = BootstrapWidget.css_classes + ('date',)


class TimeInput (BootstrapWidget, forms.TimeInput):
    """ Bootstrap version of ``forms.TimeInput``. The input is rendered with an extra "time" class. """
    css_classes = BootstrapWidget.css_classes + ('time',)


class DateTimeInput (BootstrapWidget, forms.DateTimeInput):
    """ Bootstrap version of ``forms.TimeInput``. The input is rendered with an extra "time" class. """
    css_classes = BootstrapWidget.css_classes + ('datetime',)


class Select (BootstrapWidget, forms.Select):
    """ Bootstrap version of ``forms.Select`` """
    css_classes = ('custom-select',)


class SelectMultiple (BootstrapWidget, forms.SelectMultiple):
    """ Bootstrap version of ``forms.SelectMultiple`` """
    css_classes = ('custom-select',)


class RadioSelect (BootstrapWidget, forms.RadioSelect):
    """ Bootstrap version of ``forms.RadioSelect`` """
    css_classes = ('form-check-input',)
    use_fieldset = True


class CheckboxInput (BootstrapWidget, forms.CheckboxInput):
    """ Bootstrap version of ``forms.CheckboxInput`` """
    css_classes = ('form-check-input',)


class CheckboxSelectMultiple (BootstrapWidget, forms.CheckboxSelectMultiple):
    """ Bootstrap version of ``forms.CheckboxSelectMultiple`` """
    css_classes = ('form-check-input',)
    use_fieldset = True


class NullBooleanSelect (BootstrapWidget, forms.NullBooleanSelect):
    """ Bootstrap version of ``forms.NullBooleanSelect`` """
    css_classes = ('custom-select',)

    def __init__(self, attrs=None, unknown_label=None):
        super(NullBooleanSelect, self).__init__(attrs=attrs)
        self.choices = (
            ('unknown', unknown_label or _('Unknown')),
            ('true', _('Yes')),
            ('false', _('No'))
        )


class NullBooleanRadioSelect (RadioSelect):
    """ A ``RadioSelect`` widget for ``NullBooleanField`` """

    def __init__(self, attrs=None, unknown_label=None):
        super(NullBooleanRadioSelect, self).__init__(attrs=attrs)
        self.choices = (
            ('unknown', unknown_label or _('Unknown')),
            ('true', _('Yes')),
            ('false', _('No'))
        )

    def render(self, name, value, attrs=None, renderer=None):
        try:
            value = {
                True: 'true',
                False: 'false',
                'true': 'true',
                'false': 'false',
                '2': 'true',
                '3': 'false',
            }[value]
        except KeyError:
            value = 'unknown'
        return super(NullBooleanRadioSelect, self).render(name, value, attrs, renderer=renderer)

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        return {
            '2': True,
            True: True,
            'True': True,
            'true': True,
            '3': False,
            'False': False,
            False: False,
            'false': False,
        }.get(value)


class EmailInput (TextInput):
    input_type = 'email'


class NumberInput (TextInput):
    input_type = 'number'

class URLInput (TextInput):
    input_type = 'url'

class FileInput (BootstrapWidget, forms.FileInput):
    """ Bootstrap version of ``forms.FileInput`` """
    css_classes = ()

class ModelWidgets (collections.Mapping):

    widget_map = {
       forms.TextInput: TextInput,
       forms.PasswordInput: PasswordInput,
       forms.Textarea: Textarea,
       forms.DateInput: DateInput,
       forms.TimeInput: TimeInput,
       forms.DateTimeInput: DateTimeInput,
       forms.Select: Select,
       forms.SelectMultiple: SelectMultiple,
       forms.RadioSelect: RadioSelect,
       forms.CheckboxInput: CheckboxInput,
       forms.CheckboxSelectMultiple: CheckboxSelectMultiple,
       forms.NullBooleanSelect: NullBooleanSelect,
       forms.EmailInput: EmailInput,
       forms.NumberInput: NumberInput,
       forms.URLInput: URLInput,
    }

    def __init__(self, model_class, overrides=None):
        self.model_class = model_class
        self.overrides = overrides or {}

    def __getitem__(self, key):
        if key in self.overrides:
            return self.overrides[key]
        try:
            original_widget = self.model_class._meta.get_field(key).formfield().widget
            return self.widget_map.get(original_widget.__class__, original_widget)
        except AttributeError:
            return None

    def __iter__(self):
        seen = set()
        for key in overrides:
            seen.add(key)
            yield key
        for field in self.model_class._meta.fields:
            if field.name not in seen and field.formfield():
                yield field.name

    def __len__(self):
        key_set = set(self.overrides.keys())
        key_set.update(f.name for f in self.model_class._meta.fields if f.formfield())
        return len(key_set)
