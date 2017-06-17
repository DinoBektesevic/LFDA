import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import date2num
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
from matplotlib.dates import WeekdayLocator
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import numpy as np

def stackyearsResults(Results): ##We want to forget about year separaton
    temp = list() 
    for res in Results: ##res is now a single Result from Results
        t = res.t       ##we want just the detection times!
        dt = datetime.strptime(t.ymd, "%Y-%m-%d")
        temp.append(date2num(datetime(2000, dt.month, dt.day)))
    return temp   

    
def hist_month_day(Results, bins, title=None):

    dates = stackyearsResults(Results)

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
    fig.autofmt_xdate()
    fig.set_size_inches(18.5,10.5)
    plt.show()
    #return fig


##pathres = "/home/dino/Desktop/results"
##test = results.Results(pathres)
##hist_month_day(test, 365)
##plt.show()
