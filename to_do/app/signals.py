from django.db.models.signals import pre_save , post_save, post_delete
from django.dispatch import receiver
from .models import Category , ToDo
from django.core.cache import cache

@receiver([post_delete,post_save], sender=Category)
def invalidate_cache(sender, instance, **kwargs):
    cache.delete('category_list')
    

@receiver([post_delete,post_save], sender=ToDo)
def invalidate_cache(sender, instance, **kwargs):
    cache.delete('todo_list')
    