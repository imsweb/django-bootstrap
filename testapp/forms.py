from django import forms
from bootstrap import widgets

COLOR_CHOICES = [
    ('black','Black'),
    ('blue','Blue'),
    ('brown','Brown'),
    ('green','Green'),
    ('orange','Orange'),
    ('purple','Purple'),
    ('red','Red'),
    ('yellow','Yellow'),
]

COLOR_CHOICES_WITH_EMPTY = [
    (None, '-----')
] + COLOR_CHOICES


class TestForm(forms.Form):
    "A form used to test every single django-bootstrap widget."

    textinput = forms.CharField(label='TextInput',widget=widgets.TextInput())
    autofocustextinput = forms.CharField(label='AutofocusTextInput',widget=widgets.AutofocusTextInput())
    passwordinput = forms.CharField(label='PasswordInput', widget=widgets.PasswordInput())
    textarea = forms.CharField(label='Textarea', widget=widgets.Textarea())
    dateinput = forms.CharField(label='DateInput', widget=widgets.DateInput())
    timeinput = forms.CharField(label='TimeInput', widget=widgets.TimeInput())
    datetimeinput = forms.CharField(label='DateTimeInput', widget=widgets.DateTimeInput())
    select = forms.ChoiceField(label='Select',widget=widgets.Select(), choices=COLOR_CHOICES)
    selectmultiple = forms.MultipleChoiceField(label='SelectMultiple', widget=widgets.SelectMultiple(), choices=COLOR_CHOICES)
    radioselect = forms.ChoiceField(label='RadioSelect', widget=widgets.RadioSelect(), choices=COLOR_CHOICES_WITH_EMPTY)
    checkboxinput = forms.BooleanField(label='CheckboxInput', widget=widgets.CheckboxInput())
    checkboxselectmultiple = forms.MultipleChoiceField(label='CheckboxSelectMultiple', widget=widgets.CheckboxSelectMultiple(), choices=COLOR_CHOICES)
    nullbooleanselect = forms.NullBooleanField(label='NullBooleanSelect', widget=widgets.NullBooleanSelect())
    emailinput = forms.CharField(label='EmailInput',widget=widgets.EmailInput())
    numberinput = forms.CharField(label='NumberInput',widget=widgets.NumberInput())
    urlinput = forms.CharField(label='URLInput',widget=widgets.URLInput())

    def __init__(self, *args, **kwargs):
        self.required= kwargs.pop('required',False)
        super().__init__(*args,**kwargs)
        for name, field in self.fields.items():
            self.fields[name].required = self.required

