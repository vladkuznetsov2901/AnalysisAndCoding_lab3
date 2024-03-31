from PIL import Image


def decode_bmp(encoded_image_path, output_image_path):
    encoded_image = Image.open(encoded_image_path)
    encoded_pixels = encoded_image.load()

    secret_image = Image.new("RGB", encoded_image.size)
    secret_pixels = secret_image.load()

    for x in range(encoded_image.size[0]):
        for y in range(encoded_image.size[1]):
            encoded_pixel = encoded_pixels[x, y]

            red = (encoded_pixel[0] & 0b00000011) << 6
            green = (encoded_pixel[1] & 0b00000011) << 6
            blue = (encoded_pixel[2] & 0b00000011) << 6

            secret_pixel = (red, green, blue)

            secret_pixels[x, y] = secret_pixel

    secret_image.save(output_image_path)


if __name__ == "__main__":
    encoded_image_path = "encoded_image.bmp"
    output_image_path = "decoded_secret_image.bmp"
    decode_bmp(encoded_image_path, output_image_path)
