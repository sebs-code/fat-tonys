from PIL import Image
import glob, os

size = 175, 265

for infile in glob.glob("*.jpg"):
    file, ext = os.path.splitext(infile)
    with Image.open(infile) as im:
        im = im.resize(size)  # Force resize, ignore aspect ratio
        if not file.endswith("-thumbnail"):
            im.save(file + "-thumbnail.jpg", "JPEG")
        else:
             im.save(file + '.jpg', "JPEG")
        
print('Created Thumbnails')
