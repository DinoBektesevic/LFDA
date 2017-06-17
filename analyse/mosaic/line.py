import ccd_dimensions
import numpy as np
import cv2
from point import Point
from coord_conversion import get_filter_from_int

class Line(object):
    def __init__(self, P1, P2, coordsys="frame"):

        self.coordsys = coordsys.lower()
        
        self.p1 = P1
        self.p2 = P2


    @property
    def m(self):
        #using private members of Point we get a speedup of ~2.7 times
        #(averaged over 10 measuraments) over the safe access methods
        #As long as user uses the safe setters of Point to change them
        #this is safe.
        if self.coordsys == "frame":
            return (self.p2._fy-self.p1._fy)/(self.p2._fx-self.p1._fx)
        elif self.coordsys == "ccd":
            return (self.p2._cy-self.p1._cy)/(self.p2._cx-self.p1._cx)
            

    @property
    def b(self):
        if self.coordsys == "frame":
            return self.p1._fy - (self.p2._fy-self.p1._fy)/\
                (self.p2._fx-self.p1._fx)*self.p1._fx
        elif self.coordsys == "ccd":
            return self.p1._cy - (self.p2._cy-self.p1._cy)/\
                (self.p2._cx-self.p1._cx)*self.p1._cx
            

    def gety(self, x):
        try:
            return self.m*x+self.b
        except TypeError:
            pass

        #to avoid evaluating self.m and self.b in every self.gety
        #call in a loop scenario we make local copies of variables
        #in case of an iterable input and map the function to the
        #iterable for a 10x speedup. --> from 25sec for 10mil points
        #to 2.5 sec for 10mil points.
        try:
            m = self.m
            b = self.b
            fast_gety = lambda x: m*x+b
            return map(fast_gety, x)
        except TypeError:
            pass

    def getx(self, y):
        try:
            return (y-self.b)/self.m
        except TypeError:
            pass
            
        try:
            m = self.m
            b = self.b
            fast_gety = lambda y: (y-self.b)/self.m
            return map(fast_gety, y)
        except TypeError:
            pass

            
    def __call__(self, x):
        return self.gety(x)

        
    def useCoordsys(self, coordsys):
        if coordsys.lower() in ["frame", "ccd"]:
            self.coordsys = coordsys.lower()
            self.p1.useCoordsys(self.coordsys)
            self.p2.useCoordsys(self.coordsys)

    def findEdges(self):
        currentsys = self.coordsys
        self.useCoordsys("ccd")

        maxw = ccd_dimensions.MAX_W_CCDARRAY
        maxh = ccd_dimensions.MAX_H_CCDARRAY
        
        test = ""
        res = {"x": [], "y": []}
        
        y0 = self.gety(0)
        ymax = self.gety(maxw)
        
        x0 = self.getx(0)
        xmax = self.getx(maxh)

        if x0 > 0 and x0 < maxw:
            test = "top"
            res["x"].append(x0)
        else:
            res["x"].append(0)

        if xmax > 0 and xmax < maxw:
            test += " bot"
            res["x"].append(xmax)
        else:
            res["x"].append(maxw)
            
        if y0 > 0 and y0 < maxh:
            test += " left"
            res["y"].append(y0)
        else:
            res["y"].append(0)
            
        if ymax > 0 and ymax < maxh:
            test += " right"
            res["y"].append(ymax)
        else:
            res["y"].append(maxh)

        self.useCoordsys(currentsys)

        return res


    def getCCDChips(self, step=1000):
        currentsys = self.coordsys
        self.useCoordsys("ccd")

        w_camcol = ccd_dimensions.W_CAMCOL
        w_camcol_spacing = ccd_dimensions.W_CAMCOL_SPACING
        
        h_filter = ccd_dimensions.H_FILTER
        h_filter_spacing = ccd_dimensions.H_FILTER_SPACING
        
        crossed = {1:[], 2:[], 3:[], 4:[], 5:[]}

        ranges = self.findEdges()
        if ranges["x"][0] > ranges["x"][1]:
            start = ranges["x"][1]
            stop = ranges["x"][0]
        else:
            start = ranges["x"][0]
            stop = ranges["x"][1]


        step = (stop-start)/float(step)
        
        x = np.arange(start, stop, step)
        y = self.gety(x)
                
        index = 0
        for xi in x:            
            for i in range(1, 7):
                left =  xi - (i-1) * (w_camcol + w_camcol_spacing)
                right = xi - (i-1) * (w_camcol + w_camcol_spacing) - w_camcol
                
                if (left >= 0 and left <= w_camcol and
                    right<= 0 and right >= -w_camcol):
                    
                    yi = y[index]
                    for j in range(1, 6):
                        top = yi - (j-1) * (h_filter + h_filter_spacing)
                        bot = yi - (j-1) * (h_filter + h_filter_spacing) - h_filter

                        if (top >= 0 and top <= h_filter and
                            bot <= 0 and bot >= -h_filter):
                            crossed[i].append(get_filter_from_int(j))
            index += 1

        self.useCoordsys(currentsys)
        for a in crossed:
            crossed[a] = set(crossed[a])
        return crossed
                               
                
        

    def showLine(self, color=(255,0,0), imgpath="/home/dino/Desktop/a.png"):
        img = cv2.imread(imgpath)

        currentsys = self.coordsys
        self.useCoordsys("ccd")
        
        p1 = (-10, int(self.gety(-10)))
        p2 = (21000, int(self.gety(21000)))

        for i in range(0, 30, 2):
            cv2.line(img, p1, p2, color=color, thickness=i)
            
        cv2.imwrite("/home/dino/Desktop/a.png", img,
                    [cv2.IMWRITE_PNG_COMPRESSION, 9])

        self.useCoordsys(currentsys)