def payload_from_form(form, prefix='', delete=False):
    """
    Generate a payload for a POST request based on a ModelForm
    """

    prefix = f'{prefix}-' if prefix else ''
    payload = {f'{prefix}{k}': form[k].value() for k, v in form.fields.items() if form[k].value()}
    if getattr(form.instance, 'id'):
        payload['id'] = form.instance.id

    if delete:
        payload['delete'] = True
    return payload
