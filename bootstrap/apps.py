from django.apps import AppConfig

class BootstrapConfig(AppConfig):
    name = 'bootstrap'
    
    def get_bootstrap_widget(self):
        from bootstrap.widgets import BootstrapWidget
        return BootstrapWidget