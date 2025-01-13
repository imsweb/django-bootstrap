from django.urls import include, path
from . import views

urlpatterns = [
    path('test-form/', views.test_form, name='test-form'),
]