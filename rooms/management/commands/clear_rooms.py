from django.core.management.base import BaseCommand
from rooms.models import Room, RoomType


class Command(BaseCommand):
    help = 'Delete all temporary rooms and room types'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.WARNING('⚠️  WARNING: This will delete ALL rooms and room types!'))
            response = input('Are you sure? Type "yes" to confirm: ')
            if response.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Cancelled. No data was deleted.'))
                return

        try:
            # Count before deletion
            room_count = Room.objects.count()
            room_type_count = RoomType.objects.count()

            # Delete all rooms and room types
            Room.objects.all().delete()
            RoomType.objects.all().delete()

            self.stdout.write(self.style.SUCCESS(f'✅ Successfully deleted:'))
            self.stdout.write(self.style.SUCCESS(f'   • {room_count} rooms'))
            self.stdout.write(self.style.SUCCESS(f'   • {room_type_count} room types'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
