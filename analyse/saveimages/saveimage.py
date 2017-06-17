import os
import cv2
import fitsio
import numpy as np
from sdss import files

def saveimg(run, camcol, filter, field):
    errors = open("errors.txt", "w")
#    try:
    origPathName = files.filename('frame', run=run, camcol=camcol,
                                   field=field, filter=filter)

    unpackPath = os.environ["FITSDMP"]

    fname = origPathName.split("/")[-1]
    unpackedfits = os.path.join(unpackPath, fname)
    print unpackedfits
    
    os.popen("bunzip2 -qkc "+origPathName+".bz2 >"+unpackedfits)

    #unpackedfits = "/home/dino/Desktop/boss/photoObj/frames/301/273/6/frame-i-000273-6-0116.fits"
    img = fitsio.read(unpackedfits)
    print type(img[0])
    #WARNING mirror the image vertically
    #it seems CV2 and FITSIO set different pix coords
    img = cv2.flip(img, 0)

    img[img<0.03] = 0
    img[img>0] += 100
    img[img>255] = 254
    img = cv2.convertScaleAbs(img)

    cla = cv2.equalizeHist(img)
    print cla[0]
    cla = cv2.resize(cla, (int(2048/2.56),int(1489/2.56)),
                     interpolation=cv2.INTER_AREA)
    print np.shape(cla)
    return cla
    print cv2.imwrite(os.environ["SAVEFOLDER"]+fname+".png", cla)

#    except Exception, e:
#        errors.write(str(e)+"\n\n")
#        pass
#    finally:
#        try: os.remove(unpackedfits)
#        except: pass
