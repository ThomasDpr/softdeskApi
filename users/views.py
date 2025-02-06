from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()

class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'list':
            return [IsAdminUser()]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [IsOwnerOrAdmin()]  # L'utilisateur peut modifier/supprimer son propre profil
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response(
                {'status': 'success', 'message': 'Utilisateur créé avec succès', 'data': serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response(
                {'status': 'error', 'message': 'Erreur de validation', 'errors': e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {'status': 'success', 'message': 'Liste des utilisateurs récupérée avec succès', 'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Si mon utilisateur n'est pas le propriétaire du profil je renvoie une erreur
            if request.user != instance and not request.user.is_staff:
                return Response(
                    {'status': 'error', 'message': 'Permission refusée'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {'status': 'success', 'message': 'Utilisateur mis à jour avec succès', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {'status': 'error', 'message': 'Erreur de validation', 'errors': e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if request.user != instance and not request.user.is_staff:
                return Response(
                    {'status': 'error', 'message': 'Permission refusée'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            self.perform_destroy(instance)
            return Response(
                {'status': 'success', 'message': 'Utilisateur supprimé avec succès'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {'status': 'error', 'message': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
