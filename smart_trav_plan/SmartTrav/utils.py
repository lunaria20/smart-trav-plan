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


def upload_image_to_supabase(image_file, folder_name):
    """
    Upload an image to Supabase Storage

    Args:
        image_file: Django UploadedFile object
        folder_name: Folder name in bucket (e.g., 'destinations', 'images')

    Returns:
        Public URL of the uploaded image
    """
    try:
        supabase = get_supabase_client()
        bucket_name = "destination-images"  # Your Supabase bucket name

        # Generate unique filename to avoid conflicts
        file_extension = image_file.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # Create file path
        file_path = f"{folder_name}/{unique_filename}"

        # Read file content
        file_content = image_file.read()

        print(f"Uploading {file_path} to Supabase...")  # Debug log

        # Upload to Supabase
        response = supabase.storage.from_(bucket_name).upload(
            file_path,
            file_content,
            file_options={"content-type": image_file.content_type}
        )

        print(f"Upload response: {response}")  # Debug log

        # Get public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)

        print(f"Public URL: {public_url}")  # Debug log

        return public_url

    except Exception as e:
        print(f"Error uploading to Supabase: {str(e)}")
        raise