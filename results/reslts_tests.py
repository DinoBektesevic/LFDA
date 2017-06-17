import time

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs



import sqlalchemy as sa
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .base import Base
from .frame import Frame
from .line import Line
from .linetimes import LineTime
from .point import Point
from .results import Results

#import os
#if os.path.isfile("foo1.db"):
#    os.remove("foo1.db")
#
#engine = sa.create_engine('sqlite:///foo1.db', echo=False)
#Base.metadata.create_all(engine)
#
#session = sessionmaker()
#session.configure(bind=engine)
#session = session()
#
a_result = "4822 5 r 477 4601697000.7 1025.0 745.0 352.561028128 30.5088037769 -7.56668608171e-05 7.98399411997e-05 7.98779124123e-05 7.564914539e-05 -1035.0 251.187 2065.0 -2927.0"
def parse(string):
    s = string.split(" ")
    parsed = dict()
    parsed["run"]   = int(s[0])
    parsed["camcol"]= int(s[1]) #parsed["camcol"]= s[2]
    parsed["filter"]= str(s[2]) #parsed["filter"]= s[3]
    parsed["field"] = int(s[3]) #parsed["field"] = s[1]
    if float(s[4]) == 0:
        parsed["tai"]   = float(s[5])
    else:
        parsed["tai"] = float(s[4])
    parsed["crpix1"]= float(s[5])
    parsed["crpix2"]= float(s[6])
    parsed["crval1"]= float(s[7])
    parsed["crval2"]= float(s[8])
    parsed["cd11"] = float(s[9])
    parsed["cd12"] = float(s[10])
    parsed["cd21"] = float(s[11])
    parsed["cd22"] = float(s[12])
    parsed["x1"]    = float(s[13])
    parsed["y1"]    = float(s[14])
    parsed["x2"]    = float(s[15])       
    parsed["y2"]    = float(s[16])
    return parsed

tmp = parse(a_result)

#f = Frame(tmp["run"], tmp["camcol"], tmp["filter"], tmp["field"], tmp["crpix1"],
#          tmp["crpix2"], tmp["crval1"], tmp["crval2"], tmp["cd11"], tmp["cd12"],
#          tmp["cd21"], tmp["cd22"])
#
#t = LineTime(tmp["tai"], tmp["tai"])
#
#session.add_all([f, t])
#session.commit()
#
#line = Line.fromCoords(tmp["x1"], tmp["y1"], tmp["x2"], tmp["y2"],
#                       tmp["camcol"], tmp["filter"], frame_id=f.id,
#                       linetime_id=t.id)
#
#session.add(line)
#session.commit()
#
######################################################################
######################################################################
###########################     L I N E    ###########################
###########################      TESTS     ###########################
######################################################################
######################################################################
million = range(1000000)
ten_million = range(10000000)






#with Timer() as t1:
#    for i in million:
#        Line.fromCoords(tmp["x1"], tmp["y1"], tmp["x2"], tmp["y2"],
#                        tmp["camcol"], tmp["filter"], frame_id=f.id,
#                        linetime_id=t.id)
#
#with Timer() as t2:
#    for i in million:
#        Line.fromIterableCoords((tmp["x1"], tmp["y1"]), (tmp["x2"], tmp["y2"]),
#                                tmp["camcol"], tmp["filter"], frame_id=f.id,
#                                linetime_id=t.id)
#
#with Timer() as t3:
#    for i in million:
#        p1 = Point(tmp["x1"], tmp["y1"], tmp["camcol"], tmp["filter"])
#        p2 = Point(tmp["x2"], tmp["y2"], tmp["camcol"], tmp["filter"])
#        Line(p1, p2, frame_id=f.id, linetime_id=t.id)
#
#with Timer() as t4:
#    for i in million:
#        Line(Point(tmp["x1"], tmp["y1"], tmp["camcol"], tmp["filter"]),
#             Point(tmp["x2"], tmp["y2"], tmp["camcol"], tmp["filter"]),
#             frame_id=f.id, linetime_id=t.id)
#
#
#print """\n\n################################
#Instantiation times differences for 1 000 000 instantiations
#################################"""
#print "                     seconds"
#print "fromCoords:             ", t1.msecs/1000.
#print "fromIterableCoords:     ", t2.msecs/1000.
#print "with persisting Points: ", t3.msecs/1000.
#print "without Points:         ", t4.msecs/1000.
#
#
#
#
#
#
#with Timer() as t1:
#    for i in million:
#        line.x1
#
#with Timer() as t2:
#    for i in million:
#        line.x1t
#
#print """\n\n################################
#Difference between table related lookup and Point related lookup
#No SQL SELECT performed, just direct lookup over orm.
#Remember that all line properties such as slope, intercept, a, b, c
#are table lookup properties.
#1 mil. calculations
#################################"""
#print "                     seconds"
#print "Point:           ", t1.msecs/1000.
#print "Table:           ", t2.msecs/1000.
#print "diff:            ", ((t1.msecs-t2.msecs) if (t1.msecs > t2.msecs) else (t2.msecs-t1.msecs))/1000.
#print "speedup:         ", t1.msecs/t2.msecs if (t1.msecs > t2.msecs) else t2.msecs/t1.msecs
###FOR 10 MIL LOOKUPS speedup was
##1.94915443417 and 1.92068564111 without line commited
##1.77837016019 and 2.06178165289 with line commited
##it seems as if sqlalchemy does silently query(?) for data? or is just
##that slow.
#
#
#
#
#
#
#     
#with Timer() as t2:
#    for i in million:
#        line.move(1, line.y1, line.x2, line.y2)
#
#with Timer() as t3:
#    for i in million:
#        line.move(1, 1, line.x2, line.y2)
#
#with Timer() as t4:
#    for i in million:
#        line.move(1, line.y1, 1, line.y2)
#
#with Timer() as t5:
#    for i in million:
#        line.move(1, 1, 1, line.y2)
#
#with Timer() as t6:
#    for i in million:
#        line.move(1, 1, 1, 1)
#        
#with Timer() as t7:
#    for i in million:
#        line.x1 = 1
#
#with Timer() as t8:
#    for i in million:
#        line.x1 = 1
#        line.y1 = 1
#
#with Timer() as t9:
#    for i in million:
#        line.x1 = 1
#        line.x2 = 1
#
#with Timer() as t10:
#    for i in million:
#        line.x1 = 1
#        line.y1 = 1
#        line.x2 = 1
#
#with Timer() as t11:
#    for i in million:
#        line.x1 = 1
#        line.y1 = 1
#        line.x2 = 1
#        line.y2 = 1
#
#with Timer() as t12:
#    for i in million:
#        line.p1.move(1, 1)
#
#with Timer() as t13:
#    for i in million:
#        line.p1.move(1, 1)
#        line.x2 = 1
#
#with Timer() as t13a:
#    for i in million:
#        line.p1.move(1, 1)
#        line.p2.x = 1
#
#with Timer() as t14:
#    for i in million:
#        line.p1.move(1, 1)
#        line.p2.move(1, 1)
#
#with Timer() as t1:
#    for i in million:
#        line.p1.x = 1
#
#with Timer() as t15:
#    for i in million:
#        line.p1.x = 1
#        line.p1.y = 1
#
#with Timer() as t16:
#    for i in million:
#        line.p1.x = 1
#        line.p2.x = 1
#
#with Timer() as t17:
#    for i in million:
#        line.p1.x = 1
#        line.p1.y = 1
#        line.p2.x = 1
#
#with Timer() as t18:
#    for i in million:
#        line.p1.x = 1
#        line.p1.y = 1
#        line.p2.x = 1
#        line.p2.y = 1
#
#print """\n\n################################
#Various line manipulation strategies. Moving the line from the original
#P1(x1, y1) P2(x2, y2) to:
#1.  P1 ( 1, y1 )  P2 ( x2, y2 )
#2.  P1 ( 1,  1 )  P2 ( x2, y2 )
#3.  P1 ( 1, y1 )  P2 ( 1 , y2 )
#4.  P1 ( 1,  1 )  P2 ( 1 , y2 )
#5.  P1 ( 1,  1 )  P2 ( 1 , 1  )
#by using:
#A. line single coordinate property setters (x1, y1, x2, y2)
#B. line move method
#*C. point instances move method
#*D. point instances
#
#special test cases marked with * are unsafe because data is not
#persisted torwards the DB unless some other method that calls
#_initFrame and _initCCD is accidentally called. Persisting the data
#explicitly, however, makes these methods execute within 0.1sec of the
#offered safe methods.
#
#Speedup is compared to respective coordinate change operation of
#the method bellow. So B1 is x times faster/slower than A1
#
#1 000 000 calculations.
#################################"""
#"         seconds           speedup"
#"                               B                              "
#".............................................................."
#"1.    ", t2.msecs/1000., "  ", t7.msecs/t2.msecs if (t7.msecs > t2.msecs) else t2.msecs/t7.msecs
#"2.    ", t3.msecs/1000., "  ", t8.msecs/t2.msecs if (t8.msecs > t2.msecs) else t2.msecs/t8.msecs
#"3.    ", t4.msecs/1000., "  ", t9.msecs/t2.msecs if (t9.msecs > t2.msecs) else t2.msecs/t9.msecs
#"4.    ", t5.msecs/1000., "  ", t10.msecs/t2.msecs if (t10.msecs > t2.msecs) else t2.msecs/t10.msecs
#"5.    ", t6.msecs/1000., "  ", t11.msecs/t2.msecs if (t11.msecs > t2.msecs) else t2.msecs/t11.msecs
#"                               A                              "
#".............................................................."
#"1.    ", t7.msecs/1000.
#"2.    ", t8.msecs/1000.
#"3.    ", t9.msecs/1000.
#"4.    ", t10.msecs/1000.
#"5.    ", t11.msecs/1000.
#
#print "                              C*                              "
#print ".............................................................."
#print "1.    ", "      ---    "
#print "2.    ", t12.msecs/1000., "  ", t15.msecs/t12.msecs if (t15.msecs > t12.msecs) else t12.msecs/t15.msecs
#print "3.    ", "      ---    "
#print "4.    ", t13.msecs/1000., "  ", t13.msecs/t17.msecs if (t13.msecs > t17.msecs) else t17.msecs/t13.msecs
#print "4a.    ", t13a.msecs/1000., "  ", t13a.msecs/t17.msecs if (t13a.msecs > t17.msecs) else t17.msecs/t13a.msecs
#print "5.    ", t14.msecs/1000., "  ", t18.msecs/t14.msecs if (t18.msecs > t14.msecs) else t14.msecs/t18.msecs
#print "                              D*                              "
#print ".............................................................."
#print "1.    ", t1.msecs/1000.
#print "2.    ", t15.msecs/1000.
#print "3.    ", t16.msecs/1000.
#print "4.    ", t17.msecs/1000.
#print "5.    ", t18.msecs/1000.






#with Timer() as t1:
#    for i in ten_million:
#        line(i)
#
#with Timer() as t2:
#    for i in ten_million:
#        line.calcx(i)
#
#with Timer() as t3:
#    line(ten_million)
#
#with Timer() as t4:
#    line.calcx(ten_million)
#
#print """################################
#Difference between point calculations for collections and individual
#coordinates. Individual coordinates were tested over __call__ and
#directly over getx.
#
#10 mil. calculations
################################"""
#print "                     seconds"
#print "                          __call__                            "
#print ".............................................................."
#print "individual:      ", t1.msecs/1000.
#print "map loop:        ", t3.msecs/1000.
#print "diff:            ", ((t1.msecs-t3.msecs) if (t1.msecs > t3.msecs) else (t3.msecs-t1.msecs))/1000.
#print "speedup:         ", t3.msecs/t1.msecs if (t3.msecs > t1.msecs) else t1.msecs/t3.msecs
#print "                            getx                              "
#print ".............................................................."
#print "getx:            ", t2.msecs/1000.
#print "map loop:        ", t4.msecs/1000.
#print "diff:            ", ((t4.msecs-t2.msecs) if (t4.msecs > t2.msecs) else (t2.msecs-t4.msecs))/1000.
#print "speedup:         ", t4.msecs/t2.msecs if (t4.msecs > t2.msecs) else t2.msecs/t4.msecs
#
#
#
#
#
#
#
#nelements = range(1, 11)
#nelements.extend((100, 1000, 10000))
#
#alt = []
#altc = []
#
#import operator
#
#for ii in range(100):
#    lt = []
#    for j in nelements:
#        with Timer() as t:
#            for i in range(j):
#                line(i)
#        lt.append(t.msecs)
#
#    ltc = []
#    for j in nelements:
#        span = range(j)
#        with Timer() as t:
#            line(span)
#        ltc.append(t.msecs)
#
#    if ii == 0:
#        alt.extend(lt)
#        altc.extend(ltc)
#    else:
#        map(operator.add, lt, alt)
#        map(operator.add, ltc, altc)
#
#lt = [x/3.0 for x in alt]
#ltc = [x/3.0 for x in altc]
#
#print """\n\n################################
#When Does It Pay Off To Use Collections over individual.
#
#Table shows 100 time measuraments averaged. Each measurament calculated
#the y value of the line for N elements both by iterating through the
#N x coordinates, or by maping over N x coordinates.
#
#Results are sort of biased torwards map, because creation of the list
#was not timed as calculation. It doesn't actually pay-off to create a
#list containing 1 element dynamically, only when the list was already
#created as part of an outside code is the difference visible.
#
#In any case avoiding calculations through iteration pays off due to the
#large sqlalchemy lookup overhead costs.
#
#(Table in miliseconds)
################################"""
#print "{0:6}{1:10}{2:10}{3:9}{4:8}".format("N", "Indiv.", "map", "Diff", "Sp.Up")
#for n, i, lc in zip(nelements, lt, ltc):
#   print "{0:<6}{1:<10.5}{2:<10.5}{3:<9.3}{4:<8.5}".format(
#       n, i, lc, i-lc if (i > lc) else lc-i, i/lc if (i > lc) else lc/i
#       )








######################################################################
######################################################################
####################    L I N E T I M E    ###########################
####################        TESTS          ###########################
######################################################################
######################################################################






#with Timer() as t1:
#    for i in million[:500000]:
#        LineTime(tmp["tai"], tmp["tai"])
#        
#
#with Timer() as t2:
#    for i in million[:500000]:
#        LineBasicTime(tmp["tai"],  tmp["tai"])
#
#
#print """\n\n################################
#Instantiation times differences for 1 000 000 instantiations
#################################"""
#print "                     seconds"
#print "LineTime:             ", t1.msecs/1000.
#print "LineBasicTimes:     ", t2.msecs/1000.
#print "diff:            ", ((t1.msecs-t2.msecs) if (t1.msecs > t2.msecs) else (t2.msecs-t1.msecs))/1000.
#print "speedup:         ", t1.msecs/t2.msecs if (t1.msecs > t2.msecs) else t2.msecs/t1.msecs
#






######################################################################
######################################################################
#####################    R E S U L T S    ############################
#####################        TESTS        ############################
######################################################################
######################################################################






#with Timer() as t1:
#    for i in million[:100]:
#        Results(a_result)
        
with Timer() as t1:
    a = Results.fromFile(100, a_result)

print """\n\n################################
Instantiation times differences for 1 000 000 instantiations
################################"""
print "                     seconds"
print "individual:          ", t1.msecs/1000.
#print "batch:               ", t2.msecs/1000.
#print "diff:            ", ((t1.msecs-t2.msecs) if (t1.msecs > t2.msecs) else (t2.msecs-t1.msecs))/1000.
#print "speedup:         ", t1.msecs/t2.msecs if (t1.msecs > t2.msecs) else t2.msecs/t1.msecs