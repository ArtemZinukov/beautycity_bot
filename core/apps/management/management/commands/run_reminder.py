from django.core.management.base import BaseCommand
from core.apps.reminder.main_reminder import main


class Command(BaseCommand):
    help = "Запускаем бота"

    def handle(self, *args, **options):
        main()
