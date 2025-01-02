from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def is_old_enough(self):
        if not self.date_of_birth:
            return False
        today = date.today()
        age = (today - self.date_of_birth).days / 365
        return age >= 15
