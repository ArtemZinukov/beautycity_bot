from django.core.management.base import BaseCommand
from core.apps.bot.main_bot import main


class Command(BaseCommand):
    help = "Запускаем бота"

    def handle(self, *args, **options):
        main()
