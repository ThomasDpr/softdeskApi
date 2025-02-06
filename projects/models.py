import uuid

from django.conf import settings
from django.db import models

# Create your models here.


class Project(models.Model):
    # Choix pour le type de projet
    TYPE_CHOICES = [('back-end', 'Back-end'), ('front-end', 'Front-end'), ('iOS', 'iOS'), ('Android', 'Android')]

    # Champs du projet
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_projects', verbose_name="Auteur"
    )
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.title} ({self.type})"


class Contributor(models.Model):
    # Lien vers l'utilisateur
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions')
    # Lien vers le projet
    project = models.ForeignKey(
        to='Project',  # note a moi même : on utilise 'Project' car la classe est dans le même fichier au dessus
        on_delete=models.CASCADE,
        related_name='contributors',
    )
    # Date d'ajout du contributeur
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Contrainte d'unicité pour éviter les doublons
        unique_together = ('user', 'project')
        verbose_name = "Contributeur"
        verbose_name_plural = "Contributeurs"

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"

class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High')
    ]
    
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task')
    ]
    
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished')
    ]

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        verbose_name="Priorité"
    )
    tag = models.CharField(
        max_length=7,
        choices=TAG_CHOICES,
        verbose_name="Tag"
    )
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='To Do',
        verbose_name="Statut"
    )

    # Relations
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='issues'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_issues'
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_issues'
    )

    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Problème"
        verbose_name_plural = "Problèmes"
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    


class Comment(models.Model):
    description = models.TextField(verbose_name="Description")
    
    # UUID unique généré automatiquement
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Identifiant unique"
    )
    
    # Relation avec Issue
    issue = models.ForeignKey(
        'Issue',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Issue associée"
    )
    
    # Auteur du commentaire
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Auteur"
    )
    
    # Date de création
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_time']

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.issue.title}"