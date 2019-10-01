import json

from django.contrib import messages
from django.views.generic import FormView, TemplateView


class AuthenticatedView(TemplateView, FormView):
    template_name = 'mysign_app/admin/base.html'
    model = None
    form_class = None
    list_fields = []
    json_fields = []

    def post(self, request, *args, **kwargs):
        """ Only clicked buttons get their name send, so this checks if the button with name 'delete' is pressed """
        if request.POST.get("delete"):
            self.model.objects.get(id=request.POST.get('id')).delete()
            messages.success(request, f'{self.model.class_name()} successfully deleted')
            form = self.form_class()
        else:
            """ Update the model """
            model = self.model.objects.get(id=request.POST.get('id'))
            form = self.form_class(request.POST, instance=model)
            if form.is_valid():
                form.save()
                messages.success(request, f'{self.model.class_name()} successfully created')
                form = self.form_class()

        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)

    @property
    def extra_context(self):
        return {
            'models': self._all_objects(),
            'list_fields': self.list_fields,
            'json': self.models_json(),
        }

    def models_json(self):
        objects = self._all_objects().values(*self.json_fields)
        objects = list(objects)
        return json.dumps(objects)

    def _all_objects(self):
        return self.model.objects.all()
