from django.core.management.base import BaseCommand
from SmartTrav.models import Destination
import os


class Command(BaseCommand):
    help = 'Update image URLs to use Supabase Storage'

    def handle(self, *args, **options):
        supabase_url = os.environ.get('SUPABASE_URL')
        bucket = 'destination-images'

        destinations = Destination.objects.all()
        updated = 0

        for dest in destinations:
            if dest.image and not dest.image_url:
                # Get the image path
                image_path = str(dest.image)

                # Create Supabase URL
                supabase_image_url = f"{supabase_url}/storage/v1/object/public/{bucket}/{image_path}"

                # Update the image_url field
                dest.image_url = supabase_image_url
                dest.save()

                self.stdout.write(self.style.SUCCESS(f'✓ Updated: {dest.name}'))
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'\n✓ Updated {updated} destinations'))