from django.core.management.base import BaseCommand
from SmartTrav.models import Destination
import os


class Command(BaseCommand):
    help = 'Update all destination image URLs to use Supabase Storage'

    def handle(self, *args, **options):
        supabase_url = os.environ.get('SUPABASE_URL')
        bucket = 'destination-images'

        destinations = Destination.objects.all()
        updated = 0
        skipped = 0

        for dest in destinations:
            # Check if image field has a value but image_url is empty
            if dest.image and not dest.image_url:
                # Get the image path (e.g., "images/Gaisano_Grand_Mall.jpg")
                image_path = str(dest.image)

                # Build the full Supabase URL
                full_url = f"{supabase_url}/storage/v1/object/public/{bucket}/{image_path}"

                # Update the image_url field
                dest.image_url = full_url
                dest.save()

                self.stdout.write(self.style.SUCCESS(f'✓ Updated: {dest.name}'))
                self.stdout.write(self.style.SUCCESS(f'  {full_url}'))
                updated += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'\n✓ Updated {updated} destinations'))
        self.stdout.write(self.style.WARNING(f'⊘ Skipped {skipped} destinations'))