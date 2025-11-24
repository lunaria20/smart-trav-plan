from django.core.management.base import BaseCommand
from django.conf import settings
from SmartTrav.models import Destination
import re


class Command(BaseCommand):
    help = 'Check all destination images and their URLs'

    def handle(self, *args, **kwargs):
        destinations = Destination.objects.all()

        self.stdout.write("="*80)
        self.stdout.write(self.style.SUCCESS("🖼️  IMAGE AUDIT REPORT"))
        self.stdout.write("="*80)

        # Extract project reference
        supabase_url = settings.SUPABASE_URL
        match = re.search(r'https?://(.*?)\.supabase\.co', supabase_url)
        project_ref = match.group(1) if match else 'unknown'

        self.stdout.write(f"\n📍 Project: {project_ref}")
        self.stdout.write(f"🪣 Bucket: {settings.SUPABASE_BUCKET}")
        self.stdout.write(f"\n📊 Total Destinations: {destinations.count()}")

        with_images = 0
        without_images = 0

        self.stdout.write("\n" + "="*80)
        self.stdout.write("DESTINATION IMAGES:")
        self.stdout.write("="*80)

        for dest in destinations:
            self.stdout.write(f"\n📍 {dest.name}")
            self.stdout.write(f"   ID: {dest.id}")

            if dest.image:
                with_images += 1
                self.stdout.write(self.style.SUCCESS(f"   ✓ Has image"))
                self.stdout.write(f"   📁 Path: {dest.image.name}")

                try:
                    url = dest.image.url
                    self.stdout.write(f"   🔗 URL: {url}")

                    if 'supabase.co' in url and settings.SUPABASE_BUCKET in url:
                        self.stdout.write(self.style.SUCCESS("   ✓ URL looks correct"))
                    else:
                        self.stdout.write(self.style.ERROR("   ✗ URL format seems wrong!"))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"   ✗ Error generating URL: {e}"))
            else:
                without_images += 1
                self.stdout.write(self.style.WARNING(f"   ✗ No image set"))

        self.stdout.write("\n" + "="*80)
        self.stdout.write("SUMMARY:")
        self.stdout.write("="*80)
        self.stdout.write(f"✓ With images: {with_images}")
        self.stdout.write(f"✗ Without images: {without_images}")

        if with_images > 0:
            self.stdout.write("\n" + "="*80)
            self.stdout.write("TEST A URL IN YOUR BROWSER:")
            self.stdout.write("="*80)
            first_with_image = destinations.filter(image__isnull=False).first()
            if first_with_image:
                test_url = first_with_image.image.url
                self.stdout.write(f"\nCopy this URL and test in browser:")
                self.stdout.write(self.style.WARNING(f"{test_url}"))

        self.stdout.write("\n" + "="*80)