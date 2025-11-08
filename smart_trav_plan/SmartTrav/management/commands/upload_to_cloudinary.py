from django.core.management.base import BaseCommand
from SmartTrav.models import Destination
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Upload existing destination images to Cloudinary'

    def handle(self, *args, **kwargs):
        destinations = Destination.objects.all()
        uploaded = 0
        failed = 0

        for dest in destinations:
            if dest.image:
                try:
                    # Get the current image path
                    image_path = dest.image.path
                    image_name = os.path.basename(image_path)

                    # Re-open and save (this triggers Cloudinary upload)
                    with open(image_path, 'rb') as img_file:
                        dest.image.save(image_name, File(img_file), save=True)

                    uploaded += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Uploaded: {dest.name} -> {dest.image.url}')
                    )
                except Exception as e:
                    failed += 1
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed: {dest.name} - {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⊘ Skipped: {dest.name} (no image)')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n📊 Summary: {uploaded} uploaded, {failed} failed')
        )