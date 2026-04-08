from rest_framework import permissions
from .models import User

class IsAdminUser(permissions.BasePermission):
    """
    Exige que l'utilisateur soit authentifié et ait le rôle ADMIN.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN)

class IsRecruiterUser(permissions.BasePermission):
    """
    Exige que l'utilisateur soit authentifié et ait le rôle RECRUITER.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.RECRUITER)

class IsCandidateUser(permissions.BasePermission):
    """
    Exige que l'utilisateur soit authentifié et ait le rôle CANDIDATE.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.CANDIDATE)
