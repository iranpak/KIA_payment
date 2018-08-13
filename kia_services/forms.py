import json

from django import forms

from kia_services.models import KIAServiceField


def get_form_field(service_field):
    if service_field.type == KIAServiceField.char_field:
        return forms.CharField(max_length=100, label=service_field.label)
    # TODO: complete this thing


class KIAServiceForm(forms.Form):
    def __init__(self, service, *args, **kwargs):
        super(KIAServiceForm, self).__init__(*args, **kwargs)
        service_fields = service.kiaservicefield_set.all()
        for service_field in service_fields:
            self.fields[service_field.name] = get_form_field(service_field)

    def get_json_data(self):
        data = self.cleaned_data
        json_string = json.dumps(data)
        return json_string

# TODO: adding form and template for creating services
