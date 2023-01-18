from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import TestForm


def test_form(request):
    "Display a page used for testing a form that contains every single widget."

    # if present, all fields will be required (false if not)
    required = 'required' in request.GET

    if request.method == 'POST':
        form = TestForm(data=request.POST, required=required)
        if form.is_valid():
            messages.success(request, 'Form submitted successfully.')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = TestForm(required=required)

    kwargs = {
        'form': form,
        'required': required,
    }
    return render(request, 'testapp/test_form.html', kwargs)