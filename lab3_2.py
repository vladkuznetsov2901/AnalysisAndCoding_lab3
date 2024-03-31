from PIL import Image


def encode_bmp(main_image_path, secret_image_path, output_image_path):
    main_image = Image.open(main_image_path)
    main_pixels = main_image.load()

    secret_image = Image.open(secret_image_path)
    secret_pixels = secret_image.load()

    if secret_image.size[0] > main_image.size[0] or secret_image.size[1] > main_image.size[1]:
        raise ValueError("Secret image is larger than main image")

    for x in range(secret_image.size[0]):
        for y in range(secret_image.size[1]):
            main_pixel = main_pixels[x, y]
            secret_pixel = secret_pixels[x, y]

            new_red = (main_pixel[0] & 0b11111100) | (secret_pixel[0] >> 6)
            new_green = (main_pixel[1] & 0b11111100) | ((secret_pixel[0] >> 6) & 0b00000011)
            new_blue = (main_pixel[2] & 0b11111100) | ((secret_pixel[0] >> 6) & 0b00000011)

            main_pixels[x, y] = (new_red, new_green, new_blue)

    main_image.save(output_image_path)


if __name__ == "__main__":
    main_image_path = "white.bmp"
    secret_image_path = "ulitka.bmp"
    output_image_path = "encoded_image.bmp"
    encode_bmp(main_image_path, secret_image_path, output_image_path)
