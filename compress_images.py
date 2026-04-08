from PIL import Image
import os

def convert_to_webp(image_path, quality=80):
    try:
        img = Image.open(image_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        webp_path = os.path.splitext(image_path)[0] + ".webp"
        img.save(webp_path, "WEBP", quality=quality)
        print(f"Converted {image_path} to {webp_path} successfully.")
        return webp_path
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        return None

if __name__ == "__main__":
    png_path = r"c:\dev\NGO\core\static\core\images\Generatedpic.png"
    if os.path.exists(png_path):
        size_before = os.path.getsize(png_path) / (1024 * 1024)
        print(f"PNG Size before: {size_before:.2f} MB")
        webp_path = convert_to_webp(png_path)
        if webp_path:
            size_after = os.path.getsize(webp_path) / (1024 * 1024)
            print(f"WebP Size after: {size_after:.2f} MB")
    else:
        print(f"File {png_path} not found.")
