from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserActivity, Permission, UserPermission

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User
    """
    
    password = serializers.CharField(write_only=True)
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'address', 'is_active', 'is_active_session',
            'last_activity', 'created_at', 'date_joined', 'last_login', 
            'is_staff', 'is_superuser', 'password', 'permissions'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_activity': {'read_only': True},
            'created_at': {'read_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        
        # Normaliser le nom d'utilisateur en minuscules pour cohérence avec le frontend
        if 'username' in validated_data:
            validated_data['username'] = validated_data['username'].lower()
            
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
    def get_permissions(self, obj):
        """Retourne la liste des codes de permissions de l'utilisateur"""
        try:
            permissions = obj.get_permissions()
            perm_codes = [perm.code for perm in permissions]
            print(f"DEBUG - Permissions pour {obj.username}: {perm_codes}")
            return perm_codes
        except Exception as e:
            print(f"ERREUR - get_permissions pour {obj.username}: {e}")
            return []


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer pour l'authentification
    """
    
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Compte utilisateur désactivé.')
            else:
                raise serializers.ValidationError('Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            raise serializers.ValidationError('Nom d\'utilisateur et mot de passe requis.')
        
        return data


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer pour les activités utilisateur
    """
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'user_username', 'action', 'action_display',
            'description', 'ip_address', 'user_agent', 'timestamp'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'timestamp': {'read_only': True},
        }


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer pour changer le mot de passe
    """
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Les nouveaux mots de passe ne correspondent pas.")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Ancien mot de passe incorrect.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer pour le profil utilisateur (lecture seule pour certains champs)
    """
    
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone', 'address', 'is_active_session',
            'last_activity', 'created_at'
        ]
        read_only_fields = ['username', 'role', 'last_activity', 'created_at']


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer pour les permissions
    """

    class Meta:
        model = Permission
        fields = [
            'id', 'code', 'name', 'description', 'category',
            'is_active', 'created_at'
        ]


class UserPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer pour les permissions utilisateur
    """

    permission_details = PermissionSerializer(source='permission', read_only=True)
    granted_by_username = serializers.CharField(source='granted_by.username', read_only=True)

    class Meta:
        model = UserPermission
        fields = [
            'id', 'user', 'permission', 'permission_details',
            'granted_by', 'granted_by_username', 'granted_at', 'is_active'
        ]


class UserWithPermissionsSerializer(serializers.ModelSerializer):
    """
    Serializer pour les utilisateurs avec leurs permissions
    """

    password = serializers.CharField(write_only=True, required=False)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    permissions = serializers.SerializerMethodField()
    permissions_by_category = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone', 'address', 'is_active',
            'is_active_session', 'last_activity', 'created_at',
            'date_joined', 'last_login', 'is_staff', 'is_superuser',
            'password', 'permissions', 'permissions_by_category'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'last_activity': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def get_permissions(self, obj):
        """Retourne la liste des permissions de l'utilisateur"""
        permissions = obj.get_permissions()
        return PermissionSerializer(permissions, many=True).data

    def get_permissions_by_category(self, obj):
        """Retourne les permissions groupées par catégorie"""
        return obj.get_permissions_by_category()

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        # Normaliser le nom d'utilisateur en minuscules pour cohérence avec le frontend
        if 'username' in validated_data:
            validated_data['username'] = validated_data['username'].lower()
            
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer un utilisateur avec permissions
    """

    password = serializers.CharField(write_only=True)
    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        help_text="Liste des codes de permissions à attribuer"
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'address', 'is_active', 'password', 'permissions'
        ]

    def create(self, validated_data):
        permissions_codes = validated_data.pop('permissions', [])
        password = validated_data.pop('password')

        # Normaliser le nom d'utilisateur en minuscules pour cohérence avec le frontend
        if 'username' in validated_data:
            validated_data['username'] = validated_data['username'].lower()

        # Créer l'utilisateur
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # Attribuer les permissions
        if permissions_codes:
            permissions = Permission.objects.filter(
                code__in=permissions_codes,
                is_active=True
            )

            for permission in permissions:
                UserPermission.objects.create(
                    user=user,
                    permission=permission,
                    granted_by=self.context['request'].user if 'request' in self.context else None
                )

        return user
