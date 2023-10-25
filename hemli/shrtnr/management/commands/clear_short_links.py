from django.core.management.base import BaseCommand

from hemli.shrtnr.models import ShortLink


class Command(BaseCommand):
    help = "Clears stale short links."

    def handle(self, *args, **options):
        # Найдем все сокращения, которые не принадлежат ни к какой сессии
        num_deleted, _ = ShortLink.objects.filter(sessions__isnull=True).delete()

        if num_deleted:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {num_deleted} short links')
            )
        else:
            self.stdout.write('Nothing to clear')
