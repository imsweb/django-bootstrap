ims-bootstrap Documentation
===========================

This application is a collection of Django templatetags and widgets that help output Bootstrap-ified form markup.


Examples
--------

Defining a Django form using Bootstrap widgets::

    from django import forms
    from bootstrap import widgets
    
    class RequestForm (forms.ModelForm):
        class Meta:
            model = Request
            exclude = ('type',)
            widgets = {
                'name': widgets.TextInput(attrs={'autofocus': 'autofocus'}),
                'requestor_name': widgets.TextInput,
                'abstract': widgets.Textarea,
                'studies': widgets.SelectMultiple,
            }

Alternatively, you can use the `ModelWidgets` helper to automatically create default bootstrap widgets for a form::

    class RequestForm (forms.ModelForm):
        class Meta:
            model = Request
            widgets = widgets.ModelWidgets(Request, {
                'abstract': widgets.TemplateWidget('abstract.html'), # Custom widget override
            })

Rendering a form::

    {% load bootstrap %}
    
    <form action="" method="post">
        {% bootstrap_form form %}
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>

Rendering individual fields::

    {% load bootstrap %}
    
    <div class="form-wrap clearfix">
        {% bootstrap_field form.requestor_name %}
        {% bootstrap_field form.requestor_title %}
        {% bootstrap_field form.requestor_institution %}
        {% bootstrap_field form.requestor_email %}
        {% bootstrap_field form.requestor_address %}
        {% bootstrap_field form.requestor_phone %}
        {% bootstrap_field form.requestor_fax %}
        {% bootstrap_field form.requestor_website %}
    </div>

    <div class="page-header">
        <h3>Other Fields</h3>
    </div>

    {% for field in other_form %}
        {% bootstrap_field field %}
    {% endfor %}

Rendering individual static values (i.e. read-only views)::

    {% load bootstrap %}
    
    <div class="form-wrap clearfix">
        {% render_value req "requestor_name" %}
        {% render_value req "requestor_title" %}
        {% render_value req "requestor_institution" %}
        {% render_value req "requestor_email" %}
        {% render_value req "requestor_address" %}
        {% render_value req "requestor_phone" %}
        {% render_value req "requestor_fax" %}
        {% render_value req "requestor_website" %}
    </div>


Template Tags
-------------

.. automodule:: bootstrap.templatetags.bootstrap
   :members:


Widgets
-------

.. automodule:: bootstrap.widgets
   :members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

