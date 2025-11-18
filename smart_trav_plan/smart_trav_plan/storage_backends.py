from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client
import os
import re  # Added: Import the regular expression module


class SupabaseStorage(Storage):
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket = settings.SUPABASE_BUCKET

        # Added: Extract project reference from the SUPABASE_URL
        match = re.search(r'https?://(.*?)\.supabase\.co', settings.SUPABASE_URL)
        if match:
            self.project_ref = match.group(1)
        else:
            # Fallback (Shouldn't happen if SUPABASE_URL is correct)
            self.project_ref = 'local-supabase-ref'

    def _save(self, name, content):
        """Uploads the file content to Supabase."""
        self.client.storage.from_(self.bucket).upload(name, content.read())
        return name

    def url(self, name):
        """
        Returns the permanent public URL for the file.
        This manually constructs the Supabase public URL structure, which is
        required for unauthenticated image loading in production.
        """
        # Supabase Public URL Format:
        # https://<project-ref>.supabase.co/storage/v1/object/public/<bucket-name>/<file-path>

        return (
            f"https://{self.project_ref}.supabase.co/storage/v1/object/public/"
            f"{self.bucket}/{name}"
        )

    def exists(self, name):
        """Checks if a file exists in the Supabase bucket."""
        try:
            # Using the list method to check existence is more reliable than download()
            response = self.client.storage.from_(self.bucket).list(
                path=os.path.dirname(name),
                search=os.path.basename(name)
            )
            # Check if the list contains the file we searched for
            # Note: Supabase list is sometimes inconsistent, but checking the response content helps.
            return len(response) > 0 and response[0]['name'] == os.path.basename(name)
        except Exception:
            return False