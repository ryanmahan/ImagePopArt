from PIL import Image, ImageOps, ImageDraw
import math

def greyscale(scaleby, im):  # grayscale? a vs e isnt in PEP-8

    im = ImageOps.grayscale(im)
    px = im.load()
    cir = list()

    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):
            val = px[i, j]
            if val == 0:
                radius = 0
            else:
                radius = round(val / (255 / math.sqrt(scaleby)))
                if radius % 2 == 0:
                    radius += 1

            radius += 1
            x = i * scaleby
            y = j * scaleby
            topcorner = (x - radius, y - radius)
            bottomcorner = (x + radius, y + radius)
            cir.append([topcorner, bottomcorner])

    out = Image.new("L", (im.size[0] * scaleby, im.size[1] * scaleby), 0)

    for box in cir:
        draw = ImageDraw.Draw(out)
        draw.ellipse(box, 255, 0)
        del draw

    return out

def color(scaleby, im, delta=25, spacing = None):
    px = im.load()
    cir = list()

    if spacing is None:
        spacing = (scaleby/2)-3

    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):

            pixels = breadthFirstSize(px, [i, j], delta, list(), 0, scaleby/2, (im.size[0], im.size[1]))

            # radius = len(pixels)/2
            radius = spacing

            center = (i*scaleby, j*scaleby)

            colors = [value["Color"] for value in pixels]
            reds = list(map(lambda x: x[0], colors))
            greens = list(map(lambda x: x[1], colors))
            blues = list(map(lambda x: x[2], colors))
            if reds == []:
                rgbAvg = px[i, j]
            else:
                r = round(sum(reds)/len(reds))
                g = round(sum(greens)/len(greens))
                b = round(sum(blues)/len(blues))
                rgbAvg = (r, g, b)

            topcorner = (math.floor(center[0] - radius), math.floor(center[1]-radius))
            bottomcorner = (math.floor(center[0] + radius), math.floor(center[1] + radius))

            cir.append({"Box": (topcorner, bottomcorner),"Color": rgbAvg})

    out = Image.new("RGB", (im.size[0] * scaleby, im.size[1] * scaleby))

    for circle in cir:
        draw = ImageDraw.Draw(out)
        draw.ellipse(circle["Box"], circle["Color"], circle["Color"])
        del draw

    return out

def isSimilar(p1, p2, delta):

    similarities = 0

    if type(p1) is tuple:
        for i in range(0, 3):
            if p1[i] > p2[i] - delta and p1[i] < p2[i] + delta:
                similarities += 1
    else:
        if p1 > p2 - delta and p1 < p2 + delta:
            similarities += 1


    return similarities > 1

def breadthFirstSize(px, coor, delta, queue, calls, maxsize, size):
    for xDelta in range(-1,1):
        for yDelta in range(-1,1):

            if(type(coor) == "Dict"):
                coor = coor["xy"]



            p1 = px[coor[0], coor[1]]

            x2 = coor[0]+xDelta
            y2 = coor[1]+yDelta
            if x2 < 0:
                x2 = coor[0]
            if y2 < 0 :
                y2 = coor[1]
            # if x2 > size[0]:
            #     x2 = size[0]
            # if y2 > size[1]:
            #     y2 = size[1]

            p2 = px[x2, y2]

            if isSimilar(p1, p2, delta) and calls < maxsize:
                queue.append((x2, y2))
                # a list of dicts
        if len(queue) > 0:
            return breadthFirstSize(px, queue.pop(), delta, queue, calls+1, maxsize, size) + [{"xy": (coor[0], coor[1]), "Color": p1}]
        else:
            return list()
            # base case where isSimilar is false

fp = input("Name the filepath of the image you want to PopArt: \n")

im = Image.open(fp)
scaleby = input("Input an integer that will be the scale of your output image \n"
                "Please note that the larger this int is the compute time will scale by n^2\n")
scaleby = int(scaleby)


col = input("Color or Greyscale? C/G? \n")
print("Processing please wait...")
if col is "C":
    out = color(scaleby, im)
elif col is "G":
    out = greyscale(scaleby, im)
else:
    raise Exception("Input not valid")

out.save("output.png", "PNG")
out.show()
