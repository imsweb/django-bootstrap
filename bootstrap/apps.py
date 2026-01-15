from django.apps import AppConfig


class BootstrapConfig(AppConfig):
    name = 'bootstrap'

    def get_bootstrap_widget(self):
        from bootstrap.widgets import BootstrapWidget
        return BootstrapWidget

    def get_bootstrap_field_templates(self, field, field_class, widget_class):
        return [
            'bootstrap/%s_%s.html' % (field.form.__class__.__name__.lower(), field.name),
            'bootstrap/%s_%s.html' % (field_class, widget_class),
            'bootstrap/%s.html' % field_class,
            'bootstrap/field.html',
        ]

    def modify_bootstrap_field_classes(self, classes, field):
        return classes
