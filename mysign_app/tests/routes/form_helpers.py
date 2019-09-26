def payload_from_form(form_class, model_factory, prefix=''):
    """
    Generate a payload for a POST request based on a ModelForm
    """
    form = form_class(instance=model_factory.build())

    prefix = f'{prefix}-' if prefix else ''
    return {f'{prefix}{k}': form[k].value() for k, v in form.fields.items()}
