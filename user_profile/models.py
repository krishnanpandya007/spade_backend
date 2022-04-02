from django.db import models

# Create your models here.
import string
from random import choice, choices

def get_random_verification_code():
    
    source = string.ascii_letters + string.digits

    # Default generate key with length of 5

    result = ''

    for i in range(7):
        result += choices(source)[0]

    return result


class EmailVerification(models.Model):

    email = models.EmailField(blank=False, null=False, unique=True)
    verification_code = models.CharField(default=get_random_verification_code(), max_length=7)

    def __str__(self):

        return self.email + " | " + self.verification_code

