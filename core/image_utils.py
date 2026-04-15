"""
Utility for auto-resizing uploaded images.
Resizes to fit within max dimensions while keeping the original aspect ratio (no cropping).
Also converts to optimized JPEG/WebP for smaller file sizes.
"""
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os


# Max dimensions — images larger than this will be scaled down
MAX_WIDTH = 1200
MAX_HEIGHT = 1200
# JPEG quality (1-100)
QUALITY = 85


def resize_image(image_field, max_width=MAX_WIDTH, max_height=MAX_HEIGHT, quality=QUALITY):
    """
    Resize an image to fit within max_width x max_height
    without cropping — maintains original aspect ratio.
    Returns the modified image field ready to be saved.
    """
    if not image_field:
        return image_field

    try:
        img = Image.open(image_field)
    except Exception:
        return image_field

    # Get original dimensions
    original_width, original_height = img.size

    # Skip if already within limits
    if original_width <= max_width and original_height <= max_height:
        # Still optimize the file size even if dimensions are fine
        return _optimize_image(img, image_field.name, quality)

    # Calculate new dimensions maintaining aspect ratio
    ratio = min(max_width / original_width, max_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    # Use LANCZOS for high-quality downsampling
    img = img.resize((new_width, new_height), Image.LANCZOS)

    return _optimize_image(img, image_field.name, quality)


def _optimize_image(img, filename, quality):
    """
    Convert image to RGB (if needed) and save as optimized JPEG.
    Returns an InMemoryUploadedFile ready for Django's ImageField.
    """
    # Convert RGBA/P to RGB for JPEG compatibility
    if img.mode in ('RGBA', 'P', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Save to buffer
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)

    # Change extension to .jpg
    name_without_ext = os.path.splitext(filename)[0]
    new_filename = f"{name_without_ext}.jpg"

    return InMemoryUploadedFile(
        file=output,
        field_name='image',
        name=new_filename,
        content_type='image/jpeg',
        size=sys.getsizeof(output),
        charset=None,
    )
