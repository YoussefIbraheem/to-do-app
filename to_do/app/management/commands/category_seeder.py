from django.core.management.base import BaseCommand , CommandError
from app.models import Category
from app.factories import CategoryFactory


class Command(BaseCommand):
    help = "Seed categories into the database"
    
    def handle(self, *args, **kwargs):
        factory = CategoryFactory()
        count = kwargs.get("count", 10)
        for _ in range(count):
            category_data = factory.create()
            category = Category(**category_data)
            category.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} categories"))