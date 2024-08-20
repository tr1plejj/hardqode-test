from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Subscription


def make_payment(request, course_id):
    return Subscription.objects.filter(user_id=request.user.id, course_id=course_id).exists()


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        course_id = request.path.split('/')[4]
        return request.user.is_staff or make_payment(request, course_id)

    def has_object_permission(self, request, view, obj):
        course_id = request.path.split('/')[4]
        return request.user.is_staff or make_payment(request, course_id)


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
