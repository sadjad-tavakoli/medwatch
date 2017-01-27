from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import date
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, string_concat


def get_url(image, location):
    if image and hasattr(image, 'url'):
        return image.url
    else:
        return '{}{}'.format(settings.STATIC_URL, location)


username_regex = RegexValidator(regex=r'^[-a-z0-9_]+\Z',
                                message=_('Valid characters are numbers, lowercase '
                                          'letters and dashes.'))
