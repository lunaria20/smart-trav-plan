from django.core.management.base import BaseCommand
from SmartTrav.models import Destination
from SmartTrav.utils import get_supabase_client
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Migrate local images to Supabase Storage and update image_url field'

    def handle(self, *args, **options):
        supabase = get_supabase_client()
        bucket_name = "destination-images"

        destinations = Destination.objects.all()
        migrated = 0
        failed = 0
        skipped = 0

        for dest in destinations:
            # Check if already has Supabase URL
            if dest.image_url and 'supabase.co' in dest.image_url:
                self.stdout.write(self.style.WARNING(f'⊘ Already migrated: {dest.name}'))
                skipped += 1
                continue

            # Convert ImageFieldFile to string
            image_path = str(dest.image) if dest.image else None

            if image_path and not image_path.startswith('http'):
                # This is a local file path
                local_path = os.path.join('media', image_path)

                if os.path.exists(local_path):
                    try:
                        # Read the file
                        with open(local_path, 'rb') as f:
                            file_content = f.read()

                        # Get file extension
                        file_ext = Path(local_path).suffix.lower()
                        content_types = {
                            '.jpg': 'image/jpeg',
                            '.jpeg': 'image/jpeg',
                            '.png': 'image/png',
                            '.webp': 'image/webp',
                            '.gif': 'image/gif'
                        }
                        content_type = content_types.get(file_ext, 'image/jpeg')

                        # Upload to Supabase
                        file_path = image_path  # Keep same path structure
                        supabase.storage.from_(bucket_name).upload(
                            file_path,
                            file_content,
                            file_options={"content-type": content_type, "upsert": "true"}
                        )

                        # Get public URL
                        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)

                        # Update database - use image_url field
                        Destination.objects.filter(id=dest.id).update(image_url=public_url)

                        self.stdout.write(self.style.SUCCESS(f'✓ Migrated: {dest.name} -> {file_path}'))
                        migrated += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'✗ Failed: {dest.name} - {str(e)}'))
                        failed += 1
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ File not found: {local_path}'))
                    failed += 1
            elif dest.image_url and dest.image_url.startswith('http'):
                # Keep existing external URLs (like Unsplash)
                self.stdout.write(self.style.WARNING(f'⊘ External URL kept: {dest.name}'))
                skipped += 1
            else:
                self.stdout.write(self.style.WARNING(f'⊘ No image: {dest.name}'))
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f'\n✓ Migration complete!'))
        self.stdout.write(self.style.SUCCESS(f'  Migrated: {migrated}'))
        self.stdout.write(self.style.WARNING(f'  Skipped: {skipped}'))
        self.stdout.write(self.style.ERROR(f'  Failed: {failed}'))