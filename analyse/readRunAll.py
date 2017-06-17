from detecttrails.sdss import yanny
from detecttrails.sdss import files
import os
import hist
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from matplotlib.dates import WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import numpy as np
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import astropy.time as time




"""
First plot. For plot commands and idea look at hist.py.
My recommendation is to untar it on Desktop, or manually check all the file/folder
paths!

1) Grab datetime string of each run located in photoRunAll-dr10.par file!
    They are located in the datetimes list. They look like '1998/04/19'.
2) Parse the datestring into a python datetime. This is in dates list!
3) Stack all years into 1. See hist.compress function. This also converts
    python datetime object into a float with date2num!
4) Use the same function from hist.py with different axis labels.

DO NOT IMPORT THIS AS RESULTS PACKAGE! THIS IS SPECIFIC USE ONLY!
TO DO: make a more generalized function for bar plots for results.
       Maybe a Graph class that takes Results object to make generalized graphs?
       Also a must: functions from hist.py to convert times _has_ to be included
       in Results class! SDSS times are unreadable otherwise...
"""

PHOTO_REDUX = os.environ.get("PHOTO_REDUX")
test = yanny.read(PHOTO_REDUX+"/photoRunAll-dr10.par")
test = test["photorunall"]
##
##datetimes = list()
##for t in test:
##    ymd=t["datestring"]
##    dt = datetime.strptime(ymd, "%Y/%m/%d")
##    datetimes.append(dt)
##
##dates = list()
##for res in datetimes:
##    dates.append(date2num(res))
##
##dates2 = hist.compress(datetimes)
##
def hist_month_day(dates1, dates2, bins, title=None):

    hist1, bin_edges1 = np.histogram(dates1, bins)
    hist2, bin_edges2 = np.histogram(dates2, bins)
    width1 = bin_edges1[1]-bin_edges1[0]
    width2 = bin_edges2[1]-bin_edges2[0]
    
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax2.set_ylim((0, 20))
    
    barlist2 = ax.bar(bin_edges2[:-1], hist2/width2, width=width2)
    barlist1 = ax2.bar(bin_edges1[:-1], hist1/width1, width=width1)
    

    #MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=16) 
    mpl.rc('ytick', labelsize=16)

    for bar in barlist2:
        bar.set_color("g")
    for bar in barlist1:
        bar.set_color("b")
     
    
    ax.set_ylabel("Linear features", fontsize=24)
    ax2.set_ylabel("Total observation hours", fontsize=24)
    ax.set_xlabel("Date", fontsize=24)
    if title: ax.set_title(title)
    
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%b-%d"))

    ##I CAN'T FIND A DAY THAT DOESN'T OVERLAP WITH MONTH TICKS!
##    days = WeekdayLocator(interval=5) 
##    ax.xaxis.set_minor_locator(days)
##    ax.xaxis.set_minor_formatter(DateFormatter("%d"))
##    minticks = [tick.label1.set(rotation=45, fontsize=10)
##                for tick in ax.xaxis.get_minor_ticks()]
    
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    fig.autofmt_xdate()
    fig.set_size_inches(18.5,10.5)
    return fig

##hist_month_day(dates2, hist.dates2, 365)
##plt.show()
##
















"""
Second plot. For plot commands and idea look at hist.py.
My recommendation is to untar it on Desktop, or manually check all the file/folder
paths!

1) Grab datetime string  and start/end -field of each run located in photoRunAll-dr10.par file!
    They are located in the datetimes list. They look like '1998/04/19'.
    Generally endfield-startfield is not number of fields per night!
    Frames that don't match quality requirements are dumped, but the
    number is close enough!
2) Parse the datestring into a python datetime. This is in dates list!
3) Stack all years into 1. See hist.compress function. This also converts
    python datetime object into a float with date2num!
4) A bit of fuckery now, making a histogram of dates stacks dates into bins,
    but ignores nfields. Nfields don't get stacked.
    IDEA: make dates histogram, run through unstacked dates and compare the
    date to bin edges. Bin-edges are floats stating from which to which number
    does a bin span. If a date falls into one bin, add that date's field number
    to cumulative array of field numbers.
5) Use the same function from hist.py with different axis labels, also
    bar plot for axis 2 is now given with bin_edge of all compressed dates
    (dates2) and axis 1 is dates2 from hist.py! hist.dates2 is from Alex's results!
    CHANGE THE PATH TO ALEX'S RESULTS!

DO NOT IMPORT THIS AS RESULTS PACKAGE! SPECIFIC USE ONLY!
"""


datetimes = list()
nfields = list()
##for t in test:
##    ymd=t["datestring"]
##    print ymd
##    dt = datetime.strptime(ymd, "%Y/%m/%d")
##    datetimes.append(dt)
##
##    startfield=t["startfield"]
##    endfield = t["endfield"]
##    nfields.append(endfield-startfield)

for t in test:
    ymd=t["datestring"]
    dt = datetime.strptime(ymd, "%Y/%m/%d")
    datetimes.append(dt)

    startfield=t["startfield"]
    endfield = t["endfield"]
    nfields.append(endfield-startfield)

dates = list()
for res in datetimes:
    dates.append(date2num(res))

dates2 = hist.compress(datetimes)



def binit(dates, nfields, bins):
    """****DEPRECATED****"""
    fields = np.zeros(bins)
    start = min(dates)
    width = (max(dates)-min(dates))/bins
    for i in range(bins):
        for j in range(len(dates)):
            if (dates[j]>i*width+start) and (dates[j]<=(i*width+start+width)):
                fields[i]+=nfields[j]
    return fields


def binit2(dates, nfields, bins):
    hist, bin_edges = np.histogram(dates, bins)   
    fields = np.zeros(bins)
    
    for i in range(len(nfields)-1):
        for j in range(bins-1):
            if (dates[i]>=bin_edges[j]) and (dates[i]<bin_edges[j+1]):
                fields[j]+=nfields[i]
    return fields

    
def nfields_month_day(fields, dates1, dates, bins, title=None):

    hist1, bin_edges = np.histogram(dates, bins)
    hist2, bin_edges2 = np.histogram(dates1, bins)
    width = bin_edges[1]-bin_edges[0]
    width2 = bin_edges2[1]-bin_edges2[0]


    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax2.set_ylim((0, 300))
    ax.set_ylim((0,2500))

    barlist1 = ax2.bar(bin_edges[:-1], hist1/width, width=width, label="trails")
    barlist2 = ax.bar(bin_edges2[:-1], fields, width=width2, label="frames")

    #barlist1 = ax2.bar(bin_edges2[:-1], fields, width=width2, label="frames")
    #barlist2 = ax.bar(bin_edges[:-1], hist1/width, width=width, label="trails")
    

    #MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=16) 
    mpl.rc('ytick', labelsize=16)

    for bar in barlist1:
        bar.set_color("b")
    
    for bar in barlist2:
        bar.set_color("g")
    
    ax.set_ylabel("Frames", fontsize=24)
    ax2.set_ylabel("Detections", fontsize=24)
    ax.set_xlabel("Date", fontsize=24)
    if title: ax.set_title(title)
    
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%b-%d"))

    ##I CAN'T FIND A DAY THAT DOESN'T OVERLAP WITH MONTH TICKS!
##    days = WeekdayLocator(interval=5) 
##    ax.xaxis.set_minor_locator(days)
##    ax.xaxis.set_minor_formatter(DateFormatter("%d"))
##    minticks = [tick.label1.set(rotation=45, fontsize=10)
##                for tick in ax.xaxis.get_minor_ticks()]
    
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    plt.legend((barlist1, barlist2), ("Trails", "Frames"), "upper right")
    fig.autofmt_xdate()
    fig.set_size_inches(18.5,10.5)
    return fig


fields = binit2(dates2, nfields, 365)
##nfields_month_day(fields, dates2, hist.dates2, 365)
##plt.show()



def scatter_plot(x,y,z,bins):
    hist1, bin_edges = np.histogram(y, 365)
    width = bin_edges[1]-bin_edges[0]
    hist2, bin_edges2 = np.histogram(z, 365)
    width2 = bin_edges2[1]-bin_edges2[0]
    
    fit = np.polyfit(fields, hist1/width, 1)
    fitplt = np.polyval(fit, x)

    
    fig= plt.figure()
    ax = fig.add_subplot(1,1,1)#,axisbg="#FDFDFD")

    ax.plot(x, fitplt, label="Linear fit")

    ax.scatter(x, hist1/width, s=10, facecolors="k", edgecolors="k")
    ax.scatter(x[1:7],hist1[1:7]/width, s=80, color="red", label="Nights of QUA")
    ax.scatter(x[334:340],hist1[334:340]/width, s=80, color="#00FF00", label="Nights of LEO")
    ax.scatter(x[345:350],hist1[345:350]/width, s=80, color="#DB4DDB", label="Nights of GEM")

    plt.grid()
    plt.xlabel("Frames", fontsize=24)
    plt.ylabel("Linear features", fontsize=24)
    plt.legend(loc="upper left")
    plt.ylim(-5, 250)
    plt.xlim(5, 2100)

    
    a = plt.axes([.31, .515, .45, .37])#, axisbg="#FDFDFD")
    a.scatter(x, hist2/width2, marker=".", facecolor="k", edgecolors="k")#, facecolors="none", edgecolors="k")
    a.scatter(x[1:7],hist2[1:7]/width2, s=40, color="red") #, label="Nights of QUA")
    a.scatter(x[334:340],hist2[334:340]/width2, s=40, color="#00FF00")#, label="Nights of LEO")
    a.scatter(x[345:350],hist2[345:350]/width2, s=40, color="#DB4DDB")#, label="Nights of GEM")

    fit2 = np.polyfit(fields, hist2/width2, 1)
    fitplt2 = np.polyval(fit2, x)

    a.plot(x, fitplt2, label="Linear fit")
    
    #MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=16) 
    mpl.rc('ytick', labelsize=16)

    plt.ylim(-5, 355)
    plt.xlim(4, 2100)

    plt.grid(linewidth=0.5)
    #plt.legend(loc="upper left")
    #plt.show()
    fig.set_size_inches(14,6)
    plt.savefig("/home/dino/Desktop/test.pdf", bbox_layout="tight")
    #return fig


scatter_plot(fields, hist.dates2, hist.dates21, 365)



##def scatter_plot(x,y,bins):
##    hist1, bin_edges = np.histogram(y, 365)
##    width = bin_edges[1]-bin_edges[0]
##
##    
##    fit = np.polyfit(fields, hist1/width, 1)
##    fitplt = np.polyval(fit, x)
##
##    fig, ax = plt.subplots()
##
##    ax.plot(x, fitplt, label="Linear fit")
##
##    ax.scatter(x, hist1/width, facecolors="none", edgecolors="k")
##    ax.scatter(x[1:7],hist1[1:7]/width, s=80, color="red", label="Nights of QUA")
##    ax.scatter(x[334:340],hist1[334:340]/width, s=80, color="#00FF00", label="Nights of LEO")
##    ax.scatter(x[345:350],hist1[345:350]/width, s=80, color="k", label="Nights of GEM")
##    ###FF9900
##    
##    #MAKE ME PRETTY!
##    plt.rc('text', usetex=True)
##    plt.rc('font', family='serif')
##    mpl.rc('xtick', labelsize=16) 
##    mpl.rc('ytick', labelsize=16)
##    plt.xlabel("Frames", fontsize=24)
##    plt.ylabel("Linear features", fontsize=24)
##
##    plt.ylim(-5, 200)
##    plt.xlim(5, 2100)
##
##    plt.grid()
##    plt.legend(loc="upper left")
##    #plt.show()
##    fig.set_size_inches(14,6)
##    plt.savefig("/home/dino/Desktop/test.pdf", bbox_layout="tight")
##    #return fig



#plt.scatter(fields, hist1/width)
#scatter_plot(fields, hist.dates2, hist.dates21, 365)
