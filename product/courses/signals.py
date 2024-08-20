from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        groups = Group.objects.filter(course_id=instance.course_id)
        users_in_group = groups[0].users.count()
        group_id = groups[0].id
        for group in groups:
            users_amount = group.users.count()
            if users_amount < users_in_group:
                group_id = group.id
                users_in_group = users_amount

        needed_group = Group.objects.get(id=group_id)
        needed_group.users.add(instance.user_id)
