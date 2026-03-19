from rest_framework import permissions


class IsVendorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only vendors to edit their data.
    Read only permissions are allowed to any request
    """

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'vendor')
        )

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed if the user is the vendor of the object
        return hasattr(request.user, 'vendor') and request.user.vendor == obj.vendor
