import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from SmartTrav.models import Destination


class Command(BaseCommand):
    help = 'Load destinations from CSV file'

    def handle(self, *args, **kwargs):
        # Path to CSV file
        csv_file = os.path.join(settings.BASE_DIR, 'SmartTrav', 'data', 'destinations.csv')

        self.stdout.write(self.style.WARNING(f'Loading destinations from: {csv_file}'))

        # Check if file exists
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'CSV file not found at: {csv_file}'))
            return

        # Read CSV and create destinations
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            created_count = 0
            updated_count = 0

            for row in reader:
                destination, created = Destination.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        'description': row['description'],
                        'location': row['location'],
                        'category': row['category'],
                        'price_range': row['price_range'],
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Created: {destination.name}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f'↻ Updated: {destination.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Created: {created_count}, Updated: {updated_count}'))