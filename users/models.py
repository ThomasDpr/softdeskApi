from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateField(
        verbose_name="Date de naissance",
        null=True,
        )
    can_be_contacted = models.BooleanField(
        verbose_name="Peut être contacté",
        default=False, 
        help_text="L'utilisateur accepte d'être contacté"
    )
    can_data_be_shared = models.BooleanField(
        verbose_name="Partage des données autorisé",
        default=False,
        help_text="L'utilisateur accepte le partage de ses données",
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
