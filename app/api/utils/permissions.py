from rest_framework.permissions import (
    IsAuthenticated, DjangoModelPermissions)


class IsOwner(IsAuthenticated):
    """
    Permission that checks if this object has a foreign key pointing to the
    authenticated user of this request
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# class IsProductSeller(IsAuthenticated):
#     """
#     Permission that checks if this object has a foreign key pointing to the
#     authenticated user of this request
#     """

#     def has_object_permission(self, request, view, obj):
#         try:
#             return obj.seller == request.user.seller
#         except Exception:
#             return False


class IsSeller(DjangoModelPermissions):
    """
    Permission that checks if the user is a seller
    """

    def has_permission(self, request, view):
        try:
            if request.user.seller.is_active:
                return True
            return False
        except AttributeError:
            return False


# class IsSupplierOrAdmin(IsAuthenticated):
#     """
#     Permission that checks if user is a supplier on the partner instance
#     """

#     def has_object_permission(self, request, view, obj):
#         is_supplier = obj.users.filter(id=request.user.id).exists()
#         is_admin = request.user.is_staff
#         return is_supplier or is_admin
