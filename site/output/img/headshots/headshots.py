from PIL import Image
import glob, os

size = 250, 250

for infile in glob.glob("*.png"):
    file, ext = os.path.splitext(infile)
    with Image.open(infile) as im:
        im.thumbnail(size)
        im.save(file + "-thumbnail.png", "PNG")
        
print('Created Thumbnails')
