import json

from django import forms

from kia_services.models import KIAServiceField, KIAService


def get_form_field(service_field):
    if service_field.type == KIAServiceField.char_field:
        if service_field.optional:
            return forms.CharField(max_length=100, label=service_field.label, required=False)
        else:
            return forms.CharField(max_length=100, label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.boolean_field:
        if service_field.optional:
            forms.CharField(label=service_field.label, required=False)
        else:
            return forms.CharField(label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.choice_field:
        args = service_field.args
        choices = []
        for choice in args:
            choices.append((choice, args[choice]))

        if service_field.optional:
            return forms.ChoiceField(label=service_field.label, choices=choices, required=False)
        else:
            return forms.ChoiceField(label=service_field.label, choices=choices, required=True)

    elif service_field.type == KIAServiceField.date_field:
        if service_field.optional:
            return forms.DateField(label=service_field.label, required=False)
        else:
            return forms.DateField(label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.date_time_field:
        if service_field.optional:
            return forms.DateTimeField(label=service_field.label, required=False)
        else:
            return forms.DateTimeField(label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.decimal_field:
        if service_field.optional:
            return forms.DecimalField(label=service_field.label, required=False)
        else:
            return forms.DecimalField(label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.email_field:
        if service_field.optional:
            return forms.EmailField(label=service_field.label, required=False)
        else:
            return forms.EmailField(label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.file_field:
        if service_field.optional:
            return forms.FileField(label=service_field.label, required=False)
        else:
            return forms.FileField(label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.integer_field:
        if service_field.optional:
            return forms.IntegerField(label=service_field.label, required=False)
        else:
            return forms.IntegerField(label=service_field.label, required=True)

    elif service_field.type == KIAServiceField.multiple_choice_field:
        args = json.loads(service_field.args)
        choices = []
        for choice in args:
            choices.append((choice[0], choice[1]))

        if service_field.optional:
            return forms.MultipleChoiceField(label=service_field.label, choices=choices, required=False)
        else:
            return forms.MultipleChoiceField(label=service_field.label, choices=choices, required=True)


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


class KIAServiceCreationForm(forms.ModelForm):
    class Meta:
        model = KIAService
        fields = ('name', 'label', 'details', 'image_url')
        labels = {
            'name': 'نام انگلیسی خدمت',
            'label': 'نام فارسی خدمت',
            'details': 'توضیحات خدمت',
            'image_url': 'آدرس عکس خدمت',
        }


class KIAServiceFieldCreationForm(forms.ModelForm):
    class Meta:
        model = KIAServiceField
        fields = ('name', 'label', 'type', 'optional', 'args')
        labels = {
            'name': 'نام انگلیسی فیلد',
            'label': 'نام فارسی فیلد(برای نمایش به کاربر)',
            'type': 'نوع فیلد',
            'optional': 'اختیاری بودن یا نبودن فیلد',
            'args': 'گزینه‌های فیلد',
        }

