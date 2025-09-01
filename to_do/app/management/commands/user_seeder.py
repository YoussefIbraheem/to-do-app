from django.core.management.base import BaseCommand , CommandError
from django.contrib.auth.models import User
from app.factories import UserFactory

class Command(BaseCommand):
    help = "Seed users into the database"
    
    def handle(self, *args, **options):
        factory = UserFactory()
        count = options.get("count", 10)
        for _ in range(count):
            user_data = factory.create()
            user = User.objects.create_user(**user_data)
            user.save()
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} users"))