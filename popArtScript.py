from PIL import Image, ImageOps, ImageDraw
import math

fp = input("Name the filepath of the image you want to PopArt: \n")


im = Image.open(fp)
im = ImageOps.grayscale(im)
px = im.load()

cir = list()

scaleby = 20

for i in range(0, im.size[0]):
    for j in range(0, im.size[1]):
        val = px[i, j]
        if val == 0:
            radius = 0
        else:
            radius = round(val / (255/math.sqrt(scaleby)))
            if radius % 2 == 0:
                radius += 1

        x = i*scaleby
        y = j*scaleby
        topcorner = (x - radius, y - radius)
        if radius > i:
            topcorner = (0, y - radius)
        if radius > j:
            topcorner = (x - radius, 0)
        if radius > j and radius > i:
            topcorner = (0, 0)
        bottomcorner = (x + radius, y + radius)
        cir.append([topcorner, bottomcorner])

out = Image.new("L", (im.size[0]*scaleby, im.size[1]*scaleby), 0)

for box in cir:
    draw = ImageDraw.Draw(out)
    draw.ellipse(box, 255, 0)
    del draw

out.save("output.jpg", "JPEG")
