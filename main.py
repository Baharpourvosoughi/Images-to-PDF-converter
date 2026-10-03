from pathlib import Path
from PIL import Image


def convert_images_to_pdf(image_paths: list[str], output_pdf: str) -> bool:
    """Converts a list of image files into a single PDF document.

    :param image_paths: List of file paths to images.
    :param output_pdf: Destination path for the output PDF file.
    :return: True if conversion succeeds, False otherwise.
    """
    if not image_paths:
        print("Error: No images provided.")
        return False

    images = []
    for path in image_paths:
        try:
            img = Image.open(path)
            # Convert RGBA/P to RGB (PDF format requires RGB mode)
            if img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)
        except Exception as e:
            print(f"Warning: Could not open {path}. Skipped. Reason: {e}")

    if not images:
        print("Error: No valid images found to convert.")
        return False

    # Save all loaded images into a single PDF
    first_image = images[0]
    first_image.save(output_pdf, save_all=True, append_images=images[1:])
    print(f"Success: PDF saved successfully to '{output_pdf}'")
    return True


def main():
    # Automatically scan the current directory for common image formats
    current_dir = Path(".")
    valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    image_files = sorted(
        [
            str(p)
            for p in current_dir.iterdir()
            if p.suffix.lower() in valid_extensions
        ]
    )

    if image_files:
        print(f"Found {len(image_files)} image(s): {image_files}")
        convert_images_to_pdf(image_files, "output.pdf")
    else:
        print(
            "No image files found in the current directory. Add some .jpg/.png files and retry."
        )


if __name__ == "__main__":
    main()
