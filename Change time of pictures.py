import piexif
from PIL import Image
import time
import os
import datetime


#Indonesia Jakarta is 5 hours ahead
#Bali is 6 hours ahead
#we took the plane 31/05/2017 at 07:15 local time and landed at 08:20

def shift(when, delta):
    # lets declare delta in hours
    delta=delta*3600
    format = '%Y:%m:%d %H:%M:%S'
    #divide time up in the different pieces
    when = time.strptime(when, format)
    #make it so you can calculate with it
    when = time.mktime(when)
    #add diference in time
    when += delta
    #convert back to normal
    when = time.localtime(when)
    when = time.strftime(format, when)
    return when


for subdir, dirs, files in os.walk("C:\\Users\\David\\Google Drive\\Wedding\\Pictures\\Honeymoon\\Indonesia"):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".JPG") or filepath.endswith(".jpg"):
            print(filepath)
            #fname = "IMG_2653.JPG"
            img = Image.open(filepath)
            exif = piexif.load(img.info['exif'])
            # decode necessary because you get information in bytes with a "B" in front
            try:
                when = exif['Exif'][36867].decode('utf-8')
            except :
                pass
            try:
                camera = exif['0th'][271].decode('utf-8')
            except :
                pass#break is to exit for loop
            print(when)
            print(camera)
            if camera=="Canon":
                d1 = datetime.datetime.strptime('31/05/2017 01:15:00', "%d/%m/%Y %H:%M:%S").date()
                d2 = datetime.datetime.strptime(when, "%Y:%m:%d %H:%M:%S").date()
                if d2>d1:
                    shift1 = shift(when, 6)
                    print("%s shifted 6 hours " %shift1)
                else:
                    shift1 = shift(when, 5)
                    print("%s shifted 5 hours " % shift1)
                exif["Exif"][36867] = shift1
                exif_bytes = piexif.dump(exif)
                img.save(filepath, "jpeg", exif=exif_bytes)








