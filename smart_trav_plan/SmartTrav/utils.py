from supabase import create_client
import os


def get_supabase_client():
    """Get Supabase client instance"""
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY")
    )


def upload_image_to_supabase(image_file, folder_name):
    """
    Upload an image to Supabase Storage

    Args:
        image_file: Django UploadedFile object
        folder_name: Folder name in bucket (e.g., 'destinations', 'images')

    Returns:
        Public URL of the uploaded image
    """
    supabase = get_supabase_client()
    bucket_name = "destination-images"  # Your Supabase bucket name

    # Create file path
    file_path = f"{folder_name}/{image_file.name}"

    # Read file content
    file_content = image_file.read()

    # Upload to Supabase
    supabase.storage.from_(bucket_name).upload(
        file_path,
        file_content,
        file_options={"content-type": image_file.content_type}
    )

    # Get public URL
    public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)

    return public_url