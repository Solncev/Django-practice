from django.core.exceptions import ValidationError

def validate_non_negative(value):
    if value < 0:
        raise ValidationError('%s is not non-negative' % value)