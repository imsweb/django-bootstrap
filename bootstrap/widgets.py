from django import forms
from django.template import loader, Context
from django.forms.utils import flatatt

class TemplateWidget (forms.Widget):
    template_name = None
    extra_context = {}

    def __init__(self, template_name=None, attrs=None, **extra_context):
        if template_name:
            self.template_name = template_name
        self.extra_context.update(extra_context)
        super(TemplateWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        template = loader.get_template(self.template_name)
        input_attrs = flatatt(self.build_attrs(attrs, name=name))
        params = {
            'name': name,
            'value': value,
            'attrs': input_attrs,
            'widget': self,
        }
        params.update(self.extra_context)
        return template.render(Context(params))

class BootstrapWidget (object):
    css_classes = ('form-control',)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        new_class = '%s %s' % (attrs.get('class', ''), ' '.join(self.css_classes))
        attrs['class'] = new_class.strip()
        return attrs

class TextInput (BootstrapWidget, forms.TextInput):
    pass

class Textarea (BootstrapWidget, forms.Textarea):
    pass

class DateInput (BootstrapWidget, forms.DateInput):
    css_classes = BootstrapWidget.css_classes + ('date',)

class Select (BootstrapWidget, forms.Select):
    pass

class SelectMultiple (BootstrapWidget, forms.SelectMultiple):
    pass

class NullBooleanSelect (BootstrapWidget, forms.NullBooleanSelect):
    pass
