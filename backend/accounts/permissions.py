from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    """
    Permission pour les utilisateurs authentifiés
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsAdminOrGerant(permissions.BasePermission):
    """
    Permission pour les administrateurs et gérants uniquement
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['admin', 'gerant']
        )

class IsAdmin(permissions.BasePermission):
    """
    Permission pour les administrateurs uniquement
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )

class IsOwnerOrAdminOrGerant(permissions.BasePermission):
    """
    Permission pour le propriétaire de l'objet, les admins ou gérants
    """
    def has_object_permission(self, request, view, obj):
        # Lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Écriture pour le propriétaire, admin ou gérant
        return (
            request.user and 
            request.user.is_authenticated and 
            (obj.user == request.user or request.user.role in ['admin', 'gerant'])
        )
