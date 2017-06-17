import results as res
from astropy.time import Time
from detecttrails.sdss import files
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#fl = files.runlist()
#me = res.Results("~/Desktop/run_results/large_runs/1_1_2016Full/allres")


def runlens():
    fl = files.runlist()
    tmp = {}
    for run, rerun, j, k, z, startfield, endfield, e, f in fl:
        if rerun == "301":
            tmp[run] = endfield-startfield
    return tmp

#rl = runlens()


colors = {#"quad": "#3f502e", #"#404e29", #"#89ae83", #"green"
          #"quad": "#404e29", #"#89ae83", #"green"
          "quad": "#89ae83", #"green"
          #"quad": "green"
          #"aqui": "#3d4769", #"#424c6c", #"#65acb7", #"blue"
          #"aqui": "#424c6c", #"#65acb7", #"blue"
          "aqui": "#65acb7", #"blue"
          #"aqui": "blue"
          #"pers": "#694129", #"#623824", #"#cc9d80", #"red"
          #"pers": "#623824", #"#cc9d80", #"red"
          "pers": "#cc9d80", #"red"
          #"pers": "red"
          #"leo": "#5f3a64", #"#472a51", #"#a597c0", #"magenta"
          #"leo": "#472a51", #"#a597c0", #"magenta"
          "leo": "#a597c0", #"magenta"
          #"leo": "magenta"
          "other": "gray", #"black",
          #"other": "black",
          #"fit": "#30575b" #"#273e39" #"#908661"
          "fit": "#273e39" #"#908661"
          #"fit": "#908661"
          }
edgecolors="black"#"none"

def runcount():
    n_trails = []
    n_frames = []
    color = []
    years = []
    for r in rl:
        tmp = me.get(run=int(r))
        try:
            i = tmp[0]
            t = Time(i.tai/(24.*3600.), format="mjd").iso
            ymd, hms = t.split(" ")
            years.append(ymd[:4])
            nymd = "2005"+ymd[4:]
            ttmp = nymd+" "+hms
            t = Time(ttmp, format="iso")
            if t>"2005-01-01 00:00:00" and t<"2005-01-15 00:00:00":
                color.append(colors["quad"])# quadrantids
            elif t>"2005-04-19 00:00:00" and t<"2005-04-27 00:00:00":
                color.append(colors["aqui"]) #eta aquariids
            elif t>"2005-08-13 00:00:00" and t<"2005-08-26 00:00:00":
                color.append(colors["pers"]) # perseids
            elif t>"2005-11-05 00:00:00" and t<"2005-11-10 00:00:00":
                color.append(colors["leo"]) #leonids
            else:
                color.append(colors["other"])
        except:
            color.append(colors["other"])
        n_trails.append(len(me.get(run=int(r))))
        n_frames.append(rl[r])  
                
    return n_trails, n_frames, color, years

def plot_trailsVSframes(n_trails, n_frames, years):

    
    n_frames = np.asarray(n_frames)
    n_frames = 5*6*n_frames
    ln_frames = n_frames[:, np.newaxis]
    a, _, _, _ = np.linalg.lstsq(ln_frames, n_trails)
    
    fig, ax = plt.subplots()
    
    x = np.linspace(0, 1000000, 100000)
    y = a*x
    ax.plot(x, y, label="Best Line Fit a= "+str(a[0])[:6], color=colors["fit"])
    y = (a-a/2)*x
    ax.plot(x, y, linestyle="--", color=colors["fit"])
    y = (a+a/2)*x
    ax.plot(x, y, linestyle="--", color=colors["fit"])    

    ax.scatter(n_frames, n_trails, c=color, s=80, alpha=0.4,
               edgecolors=edgecolors)
    for i in range(len(color)):
        if color[i] != colors["other"]:
            ax.scatter(n_frames[i], n_trails[i], c=color[i], s=150, alpha=1.,
                       edgecolors=edgecolors)
            #if n_trails > 200:
            #    up = n_trails[i]/20
            #else:
            #    up = -n_trails[i]/20
            #ax.text(n_frames[i], n_trails[i]+up, years[i])
            #ax.annotate(years[i], xy=(n_frames[i], n_trails[i]),
            #            xytext=(n_frames[i], n_trails[i]+up),
            #            arrowprops=dict(facecolor='black', shrink=0.005))

    ##MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=26) 
    mpl.rc('ytick', labelsize=26)

    ax.scatter(1000000, 1000000, c=colors["quad"], label="Quadrantids")
    ax.scatter(1000000, 1000000, c=colors["aqui"], label="Eta. Aquarids")
    ax.scatter(1000000, 1000000, c=colors["pers"], label="Perseids")
    ax.scatter(1000000, 1000000, c=colors["leo"], label="Leonids")
    
    
    ax.set_ylabel("$Detections$", fontsize=34)
    ax.set_xlabel("$N_{frames}$", fontsize=34)

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    ax.legend(loc="upper left", prop={'size':15}, markerscale=5)


#n_trails, n_frames, color, years = runcount()

#plot_trailsVSframes(n_trails, n_frames, years)

#plt.show()







REFSPEC_URL = 'ftp://ftp.stsci.edu/cdbs/current_calspec/1732526_nic_002.ascii'
URL = 'http://www.sdss.org/dr7/instruments/imager/filters/%s.dat'
import os

def fetch_filter(filt):
    assert filt in 'ugriz'
    url = URL % filt
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    loc = os.path.join('downloads', '%s.dat' % filt)
    if not os.path.exists(loc):
        print "downloading from %s" % url
        F = urllib2.urlopen(url)
        open(loc, 'w').write(F.read())

    F = open(loc)
        
    data = np.loadtxt(F)
    return data



def plot_totalVSactual():
    #total = {"r": (15793, len(me.get(filter="r"))),
#	 "i": (17739, len(me.get(filter="i"))),
#	 "u": (6155, len(me.get(filter="u"))),
#	 "z": (22221, len(me.get(filter="z"))),
#	 "g": (10695, len(me.get(filter="g")))
#	 }

    fig, ax = plt.subplots(2)

    left = np.asarray([3300, 4500, 5900, 7300, 8600])
    width = 500
    middle = left+width/2.

     #PLOT THE FILTERS
    for f,c in zip('ugriz', "bgrmk"):
        X = fetch_filter(f)
        ax[0].fill(X[:, 0], X[:, 1], ec=c, fc=c, alpha=0.3)

    kwargs = dict(fontsize=30, ha='center', va='center', alpha=0.5)
    ax[0].text(3500, 0.2, 'u', color='b', **kwargs)
    ax[0].text(4600, 0.2, 'g', color='g', **kwargs)
    ax[0].text(6100, 0.2, 'r', color='r', **kwargs)
    ax[0].text(7500, 0.2, 'i', color='m', **kwargs)
    ax[0].text(9000, 0.2, 'z', color='k', **kwargs)


    #PLOT THE BARS
    total_frames = [6155, 10695, 15793, 17739, 22221]
    actual_lines = [3788, 5538, 5818, 5742, 5714]

    bt = ax[1].bar(left, total_frames, color="darkgray", width=width)
    al = ax[1].bar(left, actual_lines, color="black", width=width)

    kwargs = dict(fontsize=20, ha='center', va='center')
    for x, af, tf in zip(middle, actual_lines, total_frames):
        ax[1].text(x, af-1500, af, color='w', **kwargs)
        ax[1].text(x, tf-1500, tf, color='k', **kwargs)


    ##MAKE ME PRETTY!
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    mpl.rc('xtick', labelsize=26) 
    mpl.rc('ytick', labelsize=26) 
    
    ax[0].set_ylabel("Filter Transmission", fontsize=30)
    ax[0].set_xlabel("Wavelength", fontsize=30)

    ax[0].set_xlim(3000, 10000)
    ax[1].set_xlim(3000, 10000)

    ax[1].set_ylabel("$N_{frames}$", fontsize=34)
    ax[1].set_xticks(middle)#, fontsize=28)
    ax[1].set_xticklabels(('u', 'g', 'r', 'i', 'z'), fontsize=28)

    ax[0].yaxis.grid(True)
    ax[1].yaxis.grid(True)
    
    ax[1].legend((bt, al), ("Total returned", "Actual lines"), loc="upper left",
              prop={'size':20})
    

plot_totalVSactual()
plt.show()

