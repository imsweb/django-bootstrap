# ims-bootstrap Changelog

## 1.3.0

* Added `widgets.ModelWidgets` helper to use in `Meta.widgets` to automatically create bootstrap widgets
* Changed checkbox rendering to use `label.checkbox-inline` instead of `div.checkbox` with a `label` inside
* Updated bootstrap-datepicker to version 1.6.4

## 1.3.1

* Added a standalone `glyphicons.css` file for optionally loading glyphicons (not loaded by default)

## 1.3.2

* Added a `DateTimeInput` widget

## 1.3.3

* Added `aria-describedby` attribute to fields with help text or errors

## 1.3.4

* Respect pre-existing `aria-describedby` set on widgets
* Add an `id` to each `form-group`

## 1.3.5

* Handle fields without a `formfield` in `widgets.ModelWidgets`

## 1.3.6

* Pass kwargs from `bootstrap_form`, `bootstrap_field`, and `render_value` through to the template
* Added a `render_readonly` templatetag for form fields; checks for `render_readonly` method on widgets

## 1.3.7

* Make sure hidden fields do not render a label, and do not render at all in render_readonly

## 1.3.8

* Django 1.11 compatibility

## 1.3.9

* Use `formats.date_format` in `stringify` to respect `USE_L10N`
* Escape HTML in `stringify` by default

## 1.3.10

* Bundled a copy of the latest jQuery for convenience

## 1.3.11

* Added a `django/forms/widgets/attrs.html` override to add `form-control` to Django widgets automatically

## 2.0.0

* Updated local copy of Bootstrap to v4.3.1
* Updated Datepicker for Bootstrap to v1.9.0 for Bootstrap 4 support
* Updated `bootstrap/field.html` to respect new Bootstrap 4 structure for checkboxes and radios
* Moved closing tag of `.controls.clearfix` div in `field.html` to include the errorlist so `.invalid-feedback` reacts and displays properly
* Added `widgets.CheckboxInput` which includes the proper Bootstrap 4 class
* Added `.invalid-feedback` Bootstrap 4 class to field errorlists
* Changed help-text span tags to small tags, to reflect Bootstrap 4 styles
* Updated references to Bootstrap's documentation
* Added `.page-item` and `.page-link` classes in `pager.html` where appropriate
* Restructured the `non_field_errors` alerts in `form.html` to be more Bootstrap 4 like, with a fade transition and using &times; instead of an icon font
* Gave select widgets the `custom-select` class so they style cleanly when invalid

## 2.2.0

* Updated local copy of Bootstrap to v4.4.1 while maintaining 508 compliant colors

## 4.0.0

* Updated local copy of Bootstrap v4.4.1 with contrast adjustments for default colors, navbars, breadcrumbs, and alerts
