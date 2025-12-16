from PIL import Image
import sys
import shutil

# ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
ASCII_CHARS = ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@']


class ImageToASCII:
    def __init__(self, image_path, width=100):
        self.image_path = image_path
        self.width = width
        self.aspect_ratio_factor = 0.55  # Adjust based on font aspect ratio

    def pixel_to_ascii(self, image):
        pixels = image.getdata()
        ascii_str = "".join(ASCII_CHARS[min(pixel // 25, len(ASCII_CHARS) - 1)] for pixel in pixels)
        return ascii_str

    def resize_image(self, image):
        width, height = image.size
        aspect_ratio = height / width
        new_height = int(aspect_ratio * self.width * self.aspect_ratio_factor)
        return image.resize((self.width, new_height))

    def grayscale_image(self, image):
        return image.convert("L")

    def generate_ascii(self):
        try:
            image = Image.open(self.image_path)
        except Exception as e:
            print(f"Unable to open image file {self.image_path}. {e}")
            return

        image = self.resize_image(image)
        grayscale_img = self.grayscale_image(image)
        ascii_str = self.pixel_to_ascii(grayscale_img)

        img_width = grayscale_img.width
        ascii_img = "\n".join(ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width))

        print(ascii_img)
        print("Printed ASCII image")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ascii_image.py <image_path> [width]")
        sys.exit(1)

    image_path = sys.argv[1]

    # Use provided width or default to 100
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    converter = ImageToASCII(image_path, width)
    converter.generate_ascii()