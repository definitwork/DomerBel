# from django.contrib.auth.models import Group
# from django.db import transaction
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from users.models import User


# @receiver(post_save, sender=User)
# def add_user_in_permission_group(sender: User, instance: User, **kwargs):
#     """Добавление пользователя в группу
#     с правами доступными только юр. лицам"""
#     group = Group.objects.get(name='Юридические лица')
#     if instance.entity:
#         transaction.on_commit(lambda: instance.groups.add(group))