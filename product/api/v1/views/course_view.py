from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription, CustomUser, Balance
from courses.models import Group, Lesson


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        lessons = Lesson.objects.filter(course_id=course.pk)
        return lessons


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        groups = Group.objects.filter(course_id=course.pk)
        return groups


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        user_balance = Balance.objects.get(user_id=self.request.user.id)
        course = Course.objects.get(id=pk)
        course_price = course.price
        user_subscription = Subscription.objects.filter(course_id=pk, user_id=request.user.id).exists()
        if not user_subscription:
            if user_balance.balance >= course_price:
                new_user_balance = user_balance.balance - course_price
                user_balance.balance = new_user_balance
                user_balance.save(update_fields=['balance'])
                sub = Subscription(course_id=pk, user_id=request.user.id)
                sub.save()

                groups = Group.objects.filter(course_id=course.pk)
                users_in_group = groups[0].users.count()
                group_id = groups[0].id
                for group in groups:
                    users_amount = group.users.count()
                    if users_amount < users_in_group:
                        group_id = group.id
                        users_in_group = users_amount

                needed_group = Group.objects.get(id=group_id)
                needed_group.users.add(request.user.id)

                return Response(
                    data={201: 'Done'},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                data={403: 'Insufficient funds'},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(
            data={403: 'Already in your subscription'},
            status=status.HTTP_403_FORBIDDEN
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def buy(self, request):
        user_subs = Subscription.objects.filter(user_id=request.user.id)
        courses = Course.objects.exclude(id__in=[user_sub.course_id for user_sub in user_subs])

        return Response(
            data=courses.values(),
            status=status.HTTP_200_OK
        )

