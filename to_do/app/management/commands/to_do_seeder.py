from django.core.management.base import BaseCommand , CommandError
from app.models import ToDo , Category
from app.factories import ToDoFactory , CategoryFactory
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Seed categories into the database"
    
    def handle(self, *args, **options):
        check_user = User.objects.order_by("?").filter(is_superuser=False).first()
        if not check_user:
            raise CommandError("No superuser found. Please create a user first.")
        check_category = Category.objects.order_by("?")[:3]
        if not check_category:
            raise CommandError("No categories found. Please run the category seeder first.")
        factory = ToDoFactory()
        count = options.get("count", 10)
        for _ in range(count):
            todo_data = factory.create()
            todo_data["user"] = check_user
            todo = ToDo.objects.create(**todo_data)
            todo.categories.set(check_category)
            todo.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} to-dos"))