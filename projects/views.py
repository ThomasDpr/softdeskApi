from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Comment, Contributor, Issue, Project
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    ProjectSerializer,
)

User = get_user_model()


class IsAuthor(permissions.BasePermission):
    """
    Permission personnalisée pour n'autoriser que l'auteur du projet à le modifier.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'objet est un projet ou un contributeur
        if isinstance(obj, Project):
            return obj.author == request.user
        elif isinstance(obj, Contributor):
            return obj.project.author == request.user
        return False

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets.
    Permet de créer, lire, mettre à jour et supprimer des projets.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_permissions(self):
        """
        Définit les permissions selon l'action :
        - Lecture (list, retrieve) : Être authentifié et contributeur
        - Modification/Suppression : Être l'auteur
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthor()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Retourne les projets dont l'utilisateur est l'auteur ou un contributeur.
        """
        user = self.request.user
        return Project.objects.filter(models.Q(author=user) | models.Q(contributors__user=user)).distinct()

    def perform_create(self, serializer):
        """Assigne automatiquement l'utilisateur connecté comme auteur du projet"""
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)

    def destroy(self, request, *args, **kwargs):
        """Seul l'auteur peut supprimer le projet"""
        project = self.get_object()
        if project.author != request.user:
            raise PermissionDenied("Seul l'auteur du projet peut le supprimer")
        return super().destroy(request, *args, **kwargs)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Contributor.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)

        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs")

        # Je verifie  si l'utilisateur est déjà contributeur
        user = serializer.validated_data['user']
        if Contributor.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur du projet.")

        serializer.save(project=project)

    def destroy(self, request, *args, **kwargs):
        """
        Supprime un contributeur du projet.
        Vérifie les permissions et empêche la suppression de l'auteur.
        """
        contributor = self.get_object()
        project = contributor.project

        # je verifie  que l'utilisateur actuel est l'auteur
        if project.author != request.user:
            raise PermissionDenied("Seul l'auteur du projet peut supprimer des contributeurs")

        # j'empeche la suppression de l'auteur si celui-ci est le contributeur
        if contributor.user == project.author:
            return Response(
                {"error": "Impossible de supprimer l'auteur des contributeurs"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Supprimer le contributeur
        contributor.delete()
        return Response({"message": "Contributeur supprimé avec succès"}, status=status.HTTP_200_OK)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_id)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context['project'] = get_object_or_404(Project, id=self.kwargs.get('project_pk'))
        return context

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs.get('project_pk'))
        
        # Vérifie que l'utilisateur est contributeur
        if not Contributor.objects.filter(project=project, user=self.request.user).exists():
            raise PermissionDenied("Vous devez être contributeur du projet pour créer une issue")

        serializer.save(author=self.request.user, project=project)

    def perform_update(self, serializer):
        """Seul l'auteur peut modifier l'issue"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut modifier cette issue")
        serializer.save()

    def perform_destroy(self, instance):
        """Seul l'auteur peut supprimer l'issue"""
        if instance.author != self.request.user:
            raise PermissionDenied("Seul l'auteur peut supprimer cette issue")
        instance.delete()
        
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retourne les commentaires d'une issue spécifique.
        L'utilisateur doit être contributeur du projet.
        """
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        
        # Vérifie que l'issue existe et appartient au bon projet
        issue = get_object_or_404(Issue, id=issue_id, project_id=project_id)
        
        # Vérifie que l'utilisateur est contributeur
        if not Contributor.objects.filter(
            project_id=project_id,
            user=self.request.user
        ).exists():
            raise PermissionDenied(
                "Vous devez être contributeur du projet pour voir les commentaires"
            )
            
        return Comment.objects.filter(issue_id=issue_id)

    def perform_create(self, serializer):
        """
        Crée un nouveau commentaire.
        L'utilisateur doit être contributeur du projet.
        """
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('issue_pk')
        
        project = get_object_or_404(Project, id=project_id)
        issue = get_object_or_404(Issue, id=issue_id, project=project)

        # Vérifie que l'utilisateur est contributeur
        if not Contributor.objects.filter(
            project=project,
            user=self.request.user
        ).exists():
            raise PermissionDenied(
                "Vous devez être contributeur du projet pour commenter"
            )

        serializer.save(
            author=self.request.user,
            issue=issue
        )

    def perform_update(self, serializer):
        """Seul l'auteur peut modifier le commentaire"""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                "Seul l'auteur peut modifier ce commentaire"
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Seul l'auteur peut supprimer le commentaire"""
        if instance.author != self.request.user:
            raise PermissionDenied(
                "Seul l'auteur peut supprimer ce commentaire"
            )
        instance.delete()