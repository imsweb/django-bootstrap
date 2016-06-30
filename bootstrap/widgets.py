from django import forms
from django.forms.utils import flatatt
from django.template import Context, loader
from django.utils.translation import ugettext_lazy


class TemplateWidget (forms.Widget):
    """
    A widget that renders the specified ``template_name`` with the following context
    (plus any ``extra_context``):

        name
            The name of the field
        value
            The field's current value
        attrs
            Flattened HTML attributes, computed from ``self.build_attrs``
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

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        if self.is_required:
            attrs['aria-required'] = 'true'
        attrs.update(self.extra_attrs)
        if extra_attrs:
            attrs.update(extra_attrs)
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


class Select (BootstrapWidget, forms.Select):
    """ Bootstrap version of ``forms.Select`` """


class SelectMultiple (BootstrapWidget, forms.SelectMultiple):
    """ Bootstrap version of ``forms.SelectMultiple`` """


class RadioSelect (BootstrapWidget, forms.RadioSelect):
    """ Bootstrap version of ``forms.RadioSelect`` """
    css_classes = []
    use_fieldset = True


class CheckboxSelectMultiple (BootstrapWidget, forms.CheckboxSelectMultiple):
    """ Bootstrap version of ``forms.CheckboxSelectMultiple`` """
    css_classes = []
    use_fieldset = True


class NullBooleanSelect (BootstrapWidget, forms.NullBooleanSelect):
    """ Bootstrap version of ``forms.NullBooleanSelect`` """

    def __init__(self, attrs=None, unknown_label=None):
        super(NullBooleanSelect, self).__init__(attrs=attrs)
        self.choices = (
            ('1', ugettext_lazy(unknown_label or 'Unknown')),
            ('2', ugettext_lazy('Yes')),
            ('3', ugettext_lazy('No'))
        )


class EmailInput (TextInput):
    input_type = 'email'


class NumberInput (TextInput):
    input_type = 'number'

def optional_kwarg_decorator(fn):
    """
        Decorator for decorators that will enable optional kwargs
    """

    def wrapped_decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            return fn(args[0], **kwargs)
        else:
            def real_decorator(decoratee):
                return fn(decoratee, **kwargs)

            return real_decorator

    return wrapped_decorator

@optional_kwarg_decorator
def bootstrap_form(klass, exclude=set(), exclude_predeclared_widgets=True):
    """
        Django Form class decorator to automatically attempt to convert each form field widget to bootstrap version of widget.
    """

    old_init = klass.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        auto_bootstrap_form_widgets(self, exclude=exclude, exclude_predeclared_widgets=exclude_predeclared_widgets)
    klass.__init__ = new_init
    return klass

def auto_bootstrap_form_widgets(form, exclude=set(), exclude_predeclared_widgets=True):
    """
        Attempts to convert any auto-created default django widgets to their corresponding bootstrap widget version
        By default any widgets declared explicitly via form meta's widgets dict will be excluded from conversion.
    """
    if exclude_predeclared_widgets and form._meta.widgets:
        exclude.update(form._meta.widgets.keys())
    for field_name, field in form.fields.items():
        if field_name not in exclude:
            auto_bootstrap_field_widget(field)

def auto_bootstrap_field_widget(field):
    """
        Attempts to convert django widget for field to its corresponding bootstrap widget version.
        If the field cannot be converted, the original widget is kept.
    """
    translation_map = {
       forms.TextInput: TextInput,
       forms.PasswordInput: PasswordInput,
       forms.Textarea: Textarea,
       forms.DateInput: DateInput,
       forms.TimeInput: TimeInput,
       forms.Select: Select,
       forms.SelectMultiple: SelectMultiple,
       forms.RadioSelect: RadioSelect,
       forms.CheckboxSelectMultiple: CheckboxSelectMultiple,
       forms.NullBooleanSelect: NullBooleanSelect,
       forms.EmailInput: EmailInput,
       forms.NumberInput: NumberInput,
    }
    widget_class = type(field.widget)
    if widget_class in translation_map:
        choices = getattr(field.widget, 'choices', None)
        field.widget = translation_map.get(widget_class)()
        # need to copy over choices since django pre-caches choices into widget when building form field
        if choices:
            field.widget.choices = choices

