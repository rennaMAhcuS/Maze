from PIL import Image, ImageEnhance

# Open an image file
with Image.open("../media/Images/Loading Bar.png") as img:

    r, g, b, a = img.split()

    r = ImageEnhance.Brightness(r).enhance(10)
    g = ImageEnhance.Brightness(g).enhance(10)
    b = ImageEnhance.Brightness(b).enhance(0.5)

    img = Image.merge('RGBA', (r, g, b, a))
    img.save("../media/images/IntroLoadingBar.png")
