from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import User

from .models import Comment, Contributor, Issue, Project

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['author', 'created_time']



class ContributorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'username', 'project', 'created_time']
        read_only_fields = ['created_time', 'project', 'username']

    def validate_user(self, value):
        project = self.context.get('project')
        if project and Contributor.objects.filter(project=project, user=value).exists():
            raise serializers.ValidationError("Cet utilisateur est déjà contributeur du projet")
        return value

class IssueSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    assignee_username = serializers.CharField(source='assignee.username', read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'tag',
            'priority',
            'status',
            'project',
            'author',
            'author_username',
            'assignee',
            'assignee_username',
            'created_time'
        ]
        read_only_fields = ['author', 'created_time', 'project']

    def validate_assignee(self, value):
        """
        Vérifie que l'assigné est un contributeur du projet
        """
        project = self.context.get('project')
        if project and value:
            is_contributor = Contributor.objects.filter(
                project=project,
                user=value
            ).exists()
            
            if not is_contributor:
                raise serializers.ValidationError(
                    "L'utilisateur assigné doit être un contributeur du projet"
                )
        return value
    
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    issue_title = serializers.CharField(source='issue.title', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'description',
            'uuid',
            'author',
            'author_username',
            'issue',
            'issue_title',
            'created_time'
        ]
        read_only_fields = ['author', 'uuid', 'created_time', 'issue']

    def validate_issue(self, value):
        """
        Vérifie que l'issue appartient bien au projet en cours
        et que l'utilisateur est contributeur du projet
        """
        project = self.context.get('project')
        if project and value:
            # Vérifie que l'issue appartient au bon projet
            if value.project != project:
                raise serializers.ValidationError(
                    "Cette issue n'appartient pas au projet"
                )
            
            # Vérifie que l'utilisateur est contributeur
            user = self.context['request'].user
            if not Contributor.objects.filter(project=project, user=user).exists():
                raise serializers.ValidationError(
                    "Vous devez être contributeur du projet pour commenter"
                )
        return value