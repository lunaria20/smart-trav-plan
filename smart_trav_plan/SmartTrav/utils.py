from supabase import create_client
import os
import uuid


def get_supabase_client():
    """Get Supabase client instance"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

    return create_client(url, key)


def upload_image_to_supabase(image_file, bucket_name):
    """Upload an image to Supabase Storage"""
    try:
        supabase = get_supabase_client()

        file_extension = image_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"{unique_filename}"  # Don't nest in folders

        file_content = image_file.read()

        print(f"Uploading {file_path} to bucket: {bucket_name}")

        # Use the ACTUAL bucket_name parameter, not hardcoded 'destination-images'
        response = supabase.storage.from_(bucket_name).upload(
            file_path,
            file_content,
            file_options={"content-type": image_file.content_type}
        )

        # Get public URL from the CORRECT bucket
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)

        print(f"Public URL: {public_url}")
        return public_url

    except Exception as e:
        print(f"Error uploading to Supabase: {str(e)}")
        raise