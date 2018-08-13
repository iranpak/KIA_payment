from enum import Enum

from django.db import models
from jsonfield import JSONField


# Create your models here.


class KIAService(models.Model):
    name = models.CharField(max_length=100)
    # TODO: let user insert html for details
    details = models.TextField()
    image_url = models.URLField(null=True)

    def __str__(self):
        return self.name


class KIAServiceField(models.Model):
    boolean_field = 1
    char_field = 2
    choice_field = 3
    typed_choice_field = 4
    date_field = 5
    date_time_field = 6
    decimal_field = 7
    duration_field = 8
    email_field = 9
    file_field = 10
    file_path_field = 11
    integer_field = 13
    multiple_choice_field = 14
    typed_multiple_choice_field = 15
    combo_field = 16
    TYPE_CHOICES = (
        (boolean_field, "BooleanField"),
        (char_field, "CharField"),
        (choice_field, "CharField"),
        (typed_choice_field, "TypedChoiceField"),
        (date_field, "DateField"),
        (date_time_field, "DateTimeField"),
        (decimal_field, "DecimalField"),
        (duration_field, "DurationField "),
        (email_field, "EmailField"),
        (file_field, "FileField"),
        (file_path_field, "FilePathField"),
        (integer_field, "IntegerField"),
        (multiple_choice_field, "MultipleChoiceField"),
        (typed_multiple_choice_field, "TypedMultipleChoiceField"),
        (combo_field, "ComboField")
    )

    service = models.ForeignKey(KIAService, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True)
    label = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPE_CHOICES)
    # TODO: add more field like being optional or not
    args = JSONField()

    def __str__(self):
        return format("%s: %s" % (self.service.name, self.name))


class KIATransaction(models.Model):
    registered = 1
    being_done = 2
    done = 3
    failed = 4
    STATE_CHOICES = (
        (registered, "Registered"),
        (being_done, "Being done"),
        (done, "Done"),
        (failed, "Failed")
    )

    service_name = models.CharField(max_length=100)
    # TODO: remove null=True from next field after passing login info in view
    user_mail = models.EmailField(null=True)
    state = models.IntegerField(choices=STATE_CHOICES)
    data = JSONField()

    def initialize(self, service_name):
        self.state = self.registered
        self.service_name = service_name


