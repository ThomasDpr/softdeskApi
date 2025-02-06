from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        required=True,
        error_messages={'required': 'Le nom d\'utilisateur est obligatoire.'}
    )
    password = serializers.CharField(
        write_only=True, 
        error_messages={'required': 'Le mot de passe est obligatoire.'},
    )
    date_of_birth = serializers.DateField(
        required=True,
        error_messages={'required': 'La date de naissance est obligatoire.'}
    )
    can_be_contacted = serializers.BooleanField(
        required=True,
        error_messages={'required': 'Vous devez spécifier si vous acceptez d\'être contacté.'}
    )
    can_data_be_shared = serializers.BooleanField(
        required=True,
        error_messages={'required': 'Vous devez spécifier si vous acceptez le partage de vos données.'}
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'date_of_birth',
            'can_be_contacted',
            'can_data_be_shared'
        )
    
    def to_internal_value(self, data):
        """
        Surcharge de la méthode de validation initiale des données
        """
        # Je vérifie que le corps de la requête n'est pas vide sinon je renvoie une erreur
        if not data:
            raise serializers.ValidationError({
                'error': "Le corps de la requête ne peut pas être vide"
            })

        
        # Je vérifie que l'id n'est pas présent dans le corps de la requête sinon je renvoie une erreur
        if 'id' in data:
            raise serializers.ValidationError({
                'error': "Le champ 'id' ne peut pas être modifié"
            })
        
        # Je vérifie les champs non autorisés avant toute validation
        unknown_fields = set(data.keys()) - set(self.fields.keys())
        if unknown_fields:
            raise serializers.ValidationError({
                'unknown_fields': f"Les champs suivants ne sont pas autorisés : {', '.join(unknown_fields)}"
            })
            
        return super().to_internal_value(data)
    
    def validate_date_of_birth(self, value):
        """
        Validation de l'âge de l'utilisateur (minimum 15 ans)
        """
        AGE_MINIMUM = 15
        today = date.today()
        age = int((today - value).days / 365)
        
        if age < AGE_MINIMUM:
            # Vérifie si on est en création ou en mise à jour
            if self.instance is None:  # Création
                message = f"L'utilisateur doit avoir au moins {AGE_MINIMUM} ans pour s'inscrire."
            else:  # Mise à jour
                message = f"L'âge minimum autorisé est de {AGE_MINIMUM} ans."
                
            raise serializers.ValidationError(message)
        return value

    def create(self, validated_data):
        """
        Création d'un nouvel utilisateur
        """
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Mise à jour d'un utilisateur avec hashage du mot de passe si fourni
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)  # Hash le mot de passe grâce à Django
        
        # Pour chaque champ dans l'obj validated_data je met a jour l'instance 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance