from PIL import Image
import os
print(os.getcwd())

original_image = Image.open('../media/Images/MusicOn.png')

original_image = original_image.convert("RGBA")

width, height = original_image.size
new_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

for x in range(width):
    for y in range(height):
        r, g, b, a = original_image.getpixel((x, y))
        if not (r <= 100 and g <= 100 and b <= 100):
            new_image.putpixel((x, y), (r, g, b, a))

new_image.save('../../media/images/Buttons/MusicOn.png')
