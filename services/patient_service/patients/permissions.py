from rest_framework.permissions import SAFE_METHODS, BasePermission

STAFF_ROLES = {"admin", "doctor", "receptionist"}


def has_staff_role(user):
    return getattr(user, "role", None) in STAFF_ROLES


class IsHospitalStaff(BasePermission):
    def has_permission(self, request, view):
        allowed = bool(request.user and request.user.is_authenticated and has_staff_role(request.user))
        if not allowed and request.user and request.user.is_authenticated:
            self.message = (
                "This action requires a staff role (admin/doctor/receptionist). "
                f"Your token role is '{getattr(request.user, 'role', None)}'."
            )
        return allowed


class IsAdminOrReceptionist(BasePermission):
    def has_permission(self, request, view):
        allowed = bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) in {"admin", "receptionist"}
        )
        if not allowed and request.user and request.user.is_authenticated:
            self.message = (
                "This action requires the admin or receptionist role. "
                f"Your token role is '{getattr(request.user, 'role', None)}'."
            )
        return allowed


class IsStaffOrOwner(BasePermission):
    """Staff may do anything; patients get read access to their own active record only."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return has_staff_role(request.user)

    def has_object_permission(self, request, view, obj):
        if has_staff_role(request.user):
            return True
        if request.method not in SAFE_METHODS:
            return False
        return obj.is_active and obj.auth_user_id == request.user.id
