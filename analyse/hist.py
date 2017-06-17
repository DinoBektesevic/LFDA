import astropy.time as time
from astropy.time import Time
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import date2num, num2date
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from matplotlib.dates import WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import numpy as np


"""
Lest you forget!
this is the deal, SDSS TAI times are weird!
It doens't even apply that TAI is just UTC+34sec!

or smnt like that.
This is what you do.
1) Read in Alex's results
2) run through them and grab everything into a list( dict() ). This is done in readAlex.
   2.1) Convert the times in list( dict() ) to Modified Julian Date as stated
        at http://www.sdss3.org/dr10/help/glossary.php#T
        This gets done with Alex2MDJ. Each particular time is converted with
        Tai2MDJ
3) Take the converted to MDJ data from Alex2MDJ and
   convert them to standard time strings (ISO). This is done with Alex2ISO.

Now we have a list(  dict()  ) where the TAI has been converted to ISO time.
ISO time from Astropy is a string that looks like: '1998-09-19 08:37:54.780'

4) Matplotlib doesn't understand that. Convert the string to a python.datetime
   instance. Loop through all dict's in list and grab only the ISO string.
   Split the string into two '1998-09-19' and '08:37:54.780'. Discard the h:m:s.
   Create datetime object from yyyy-mm-dd with datetime.strptime(ymd, "%Y-%m-%d").
   This gets stored into the datetimes list!
5) Matplotlib can't handle that either! Use date2num to convert the datetime objects
   to floats. They are days since UTC 1-1-0001. STOOOOPID: but maybe important:
   ***************************************************************************************
   **    Return value is a floating point number (or sequence of floats)                **
   **    which gives the number of days (fraction part represents hours,                **
   **    minutes, seconds) since 0001-01-01 00:00:00 UTC, *plus* *one*.                 **
   **    The addition of one here is a historical artifact.  Also, note                 **
   **    that the Gregorian calendar is assumed; this is not universal practice         **
   ***************************************************************************************
   This is stored in list dates!
6) Plot the list dates as histogram with hist_year_month_day. They are better sorted
   by numpy's histogram function (because mpl is stooopid!). Draw numpy hist using matplolib
   bar graph! Use the Year/Month-Locator to find where your labels should be.
   Use the DateFormatter to convert them to readable form.
   (What is plotted are actually binned date2num values!)
7) That graph makes no sense! Better to see cumulative data of all years.
   From datetimes (list of datetimeobjects) we create a new list where we change all the
   years to a common year. Now all the data remains in the same month/day, but all years
   are set to 2000. When we make a histogram out of that, numpy binns the data cumulatively.
   We've unified all years into one!
   I want to add days, can't find a day that doesn't overlap with any of the month ticks!
   stoooopid matplolib!

Don't do this ever again!
"""    


def readAlex(filepath):
    res = list(dict())
    for line in open(filepath):
        s = line.split(" ")
        res.append({"run":s[1], "field":s[2], "camcol":s[4], "camrow":s[3],
                        "filter":s[5], "tai":s[6], "CRPIX1":s[7], "CRPIX2":s[8],
                        "CRVAL1":s[9], "CRVAL2":s[10], "CD1_1":s[11],
                        "CD1_2":s[12], "CD2_1":s[13], "CD2_2":s[14],
                        "a":s[15], "b":s[16], "x1":s[17], "y1":s[18],
                        "x2":s[19], "y2":s[20], "checked":s[21], "intersectoins":s[22]})
    return res

def Tai2MJD(tai):
    if(type(tai)is not float):
        tai = float(tai)
    return tai/(24*3600)

def Alex2MJD(listdict):
    temp = list()
    for res in listdict:
        t = res.copy()
        temp.append(t)
    for res in temp:
        res["tai"]=Tai2MJD(res["tai"])      
    return temp

def Alex2ISO(listdict):
    temp = Alex2MJD(listdict)
    for res in temp:
        convert = res["tai"]
        t = Time(convert, format="mjd") #, scale="utc"
        res.pop("tai", None)
        res["iso"] = t.iso
    return temp

        
def hist_year_month_day(dates, bins, title=None):

    hist, bin_edges = np.histogram(dates, bins) ##sort the data into bins
    width = bin_edges[1]-bin_edges[0] ##width of the 1st bin is the width of all bins
    
    fig, ax = plt.subplots()

    barlist = ax.bar(bin_edges[:-1], hist/width, width=width) ##create a bar graph! Not a hist!
                   ##left bin edge   bar height  bar width    ##hist data comes from numpy!

    ##MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=16) 
    mpl.rc('ytick', labelsize=16)
    
    for bar in barlist:
        bar.set_color("k") 
    
    ax.set_ylabel("Detections", fontsize=24)
    ax.set_xlabel("Date", fontsize=24)
    if title: ax.set_title(title)
    
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))

    months = MonthLocator(bymonthday=1, interval=3)
    monthsFmt = DateFormatter("%b")
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_minor_formatter(monthsFmt)

    minticks = [tick.label1.set(rotation=45, fontsize=8) ##plt.xticks command only rotates
                for tick in ax.xaxis.get_minor_ticks()] ##major ticks! All other ticks have to
                                                        ##be manually rotated
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    ax.autoscale_view() #I don't know this does
    fig.autofmt_xdate() #this either...
    plt.xticks(rotation=45)
    return fig

def hist_month_day2(dates, bins, title=None): ##WORKING SAVE! ADD ANNOTATIOSN!

    hist, bin_edges = np.histogram(dates, bins)
    width = bin_edges[1]-bin_edges[0]
    
    fig, ax = plt.subplots()

    barlist = ax.bar(bin_edges[:-1], hist/width, width=width) #the same thing as above

    #MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=16) 
    mpl.rc('ytick', labelsize=16)
    
    for bar in barlist:
        bar.set_color("k") 
    
    ax.set_ylabel("Detections", fontsize=24)
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
    plt.ylim(0, 400)
    fig.autofmt_xdate()
    fig.set_size_inches(18.5,10.5)
    return fig
















def hist_month_day(dates, bins, title=None):

    hist, bin_edges = np.histogram(dates, bins)
    width = bin_edges[1]-bin_edges[0]
    
    fig, ax = plt.subplots()

    barlist = ax.bar(bin_edges[:-1], hist/width, width=width) #the same thing as above

    #MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=16) 
    mpl.rc('ytick', labelsize=16)
    
    for bar in barlist:
        bar.set_color("k") 
    
    ax.set_ylabel("Detections", fontsize=24)
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

    #13.8 Perseids
    perseids = datetime(year=2000, month=8, day=13)
    plt.annotate("Perseids",
                 xy=(date2num(perseids), 3),
                 xytext=(date2num(perseids)-10, 380),
                 arrowprops=dict(arrowstyle="->")
                )

    
    
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    plt.ylim(0, 400)
    fig.autofmt_xdate()
    fig.set_size_inches(18.5,10.5)
    return fig
        
test = readAlex("/home/dino/Desktop/run_results/fixed") ##from the top: read in Alex's data in a list( dict() )
ISO = Alex2ISO(test) ##create a new list( dict() ) with test[i]["tai"] times converted
                    ##to ISO times


##datetimes = list() ##Grab just the ISO times from all the data!
##for res in ISO:
##    ymd = res["iso"].split(" ")[0] ##get them as datetime objects!
##    hms = res["iso"].split(" ")[1]
##    hms = hms.split(".")[0]
##    h= datetime.strptime(hms, "%H:%M:%S")
##    if h.hour<12:
##        dt = datetime.strptime(ymd, "%Y-%m-%d")
##        test = date2num(dt)-1
##        datetimes.append(num2date(test))
##    else:
##        dt = datetime.strptime(ymd, "%Y-%m-%d")
##        datetimes.append(dt)

datetimes = list() ##Grab just the ISO times from all the data!
for res in ISO:
    ymd = res["iso"].split(" ")[0] ##get them as datetime objects!
    dt = datetime.strptime(ymd, "%Y-%m-%d")
    datetimes.append(dt)
        

dates = list() ##mpl doesn't get datetime, so convert them to 
for res in datetimes: ##float numbers of days since 01-01-0001 00:00:00UTC
    dates.append(date2num(res)) ##times are separated by year-month-day


def compress(listdict): ##We want to forget about year separaton
    temp = list() 
    for res in listdict: ##so we set all datetime object to the same year
        temp.append(date2num(datetime(year=2000, month=res.month, day=res.day)))
    return temp   
    

dates2 = compress(datetimes) ##now our data is only separated by month-day

##hist_year_month_day(dates, 4070)
##plt.show()
##
##
#hist_month_day(dates2, 365) ##plot that shit binned in 365 days! Now each bar is about 1 day.
##plt.show()









test1 = readAlex("/home/dino/Desktop/run_results/fixed")
ISO1 = Alex2ISO(test1)


datetimes1 = list() ##Grab just the ISO times from all the data!
for res in ISO1:
    ymd = res["iso"].split(" ")[0] ##get them as datetime objects!
    dt = datetime.strptime(ymd, "%Y-%m-%d")
    datetimes1.append(dt)
        

dates1 = list() ##mpl doesn't get datetime, so convert them to 
for res in datetimes1: ##float numbers of days since 01-01-0001 00:00:00UTC
    dates1.append(date2num(res)) ##times are separated by year-month-day


def compress(listdict): ##We want to forget about year separaton
    temp = list() 
    for res in listdict: ##so we set all datetime object to the same year
        temp.append(date2num(datetime(year=2000, month=res.month, day=res.day)))
    return temp   
    

dates21 = compress(datetimes1) ##now our data is only separated by month-day


##hist_month_day(dates21, 365) ##plot that shit binned in 365 days! Now each bar is about 1 day.
##plt.show()



