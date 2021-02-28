from django import template

register = template.Library()

@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    # If the form is not bound then no validity
    # css is added to this string variable
    css_class = ''
    if bound_field.form.is_bound:
        # If the field is bound (contains data) and 
        # contains errors add the css class "is-invalid"
        if bound_field.errors:
            css_class = 'is-invalid'
        # As Django never returns the data of the password field
        # to the client, we do not add any validity css to it
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)