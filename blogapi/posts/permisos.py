from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Todo el mundo tiene permisos de lectura: GET, HEAD y OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo si el usuario es el autor del Post se puede manipular el registro
        return obj.author == request.user