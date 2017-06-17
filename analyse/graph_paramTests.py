import results as res
import matplotlib.pyplot as plt
from copy import deepcopy
import os

#r = res.Results("~/Desktop/fixed", alex=True)
#dro =
#res.Results("~/Desktop/params_checks/bright/false_positives/dro10/")
#len(dro.get()) #1059

def getruns(results):
    allruns = results.get(("run",))
    allruns = [x for x, in allruns]
    noduplicates = set(allruns)
    print len(noduplicates)
    return list(noduplicates)

jobruns = [94, 4822, 4828, 4832, 4868, 2888, 5183, 3031, 1119, 1120, 1133, 1142, 1332, 1334, 1336, 1339, 7699]

def parseActualCumulative(path):
    name = ""
    data = {}
    for line in open(path).readlines():
        if line[0] == "#":
            pass
        elif line[0].isalpha():
            name = line.strip()
            data[name] = {"val":[], "total":[]}
        if line[0].isdigit():
            val, total = line.split(" ")
            data[name]["val"].append(float(val))
            data[name]["total"].append(float(total))
    return data

def prepForPlot(data):
    d = deepcopy(data)
    for param in d:
        if param != "benchmark":
            w = abs(d[param]["val"][0]-d[param]["val"][1])/2.0
            shift = w/2.0
            d[param]["val"] = [x-shift for x in d[param]["val"]]
    return d

def normalizeActual(data):
    normed = deepcopy(data)
    for key in data:
        for n in range(len(data[key]["total"])):
            normed[key]["total"][n] /= 15010
    return normed

def plot1(data, param):
    data = normalizeActual(data)
    data = prepForPlot(data)
    d = data[param]

    fig, ax = plt.subplots()

    w = abs(d["val"][0]-d["val"][1])/2.0
    ymin, ymax = min(d["total"])-0.01, max(d["total"])+0.01

    ax.bar(d["val"], d["total"], color="black", width=w,
           label=r"$N_{detected}/N_{total}$")
    
    ax.set_ylim(ymin, ymax)
    
    ax.set_title(param, {"fontsize":30})

    ax.set_ylabel(r"$N_{detected}/N_{total}$", {"fontsize":22})
    ax.set_xlabel("Parameter values", {"fontsize":22})

    ax.legend()
    fig.set_tight_layout(True)
    ax.grid()

def plotactual(param):
    data = parseActualCumulative("/home/dino/Desktop/run_results/params_checks/bright/actual/cumulative")
    plot1(data, param)
    plt.show()













    
def n_detections_for_runs(alex, runs):
    n = 0
    for run in runs:
        n += len(alex.get(run=run))
    return n

#n_detections_for_runs(r, jobruns)
#398

def split_actual_from_fp(alex, results):
    actual = 0
    fp = 0
    for tmp in results.get():
        if len(alex.get(run=tmp.run, camcol=tmp.camcol, filter=tmp.filter, field=tmp.field)) == 0:
            fp+= 1
        else:
            actual += 1
    return actual, fp

def compileresults(path):
    jobruns = [94, 4822, 4828, 4832, 4868, 2888, 5183, 3031, 1119, 1120, 1133, 1142, 1332, 1334, 1336, 1339, 7699]
    alex = res.Results(respath="/home/dino/Desktop/fixed", alex=True)
    ntotaltrails = 398
    for (dirpath, dirnames, filenames) in os.walk(path):
            for dirname in dirnames:
                data = res.Results(respath=os.path.join(path, dirname))
                actual, fp = split_actual_from_fp(alex, data)
                print "{} {} {} {} {}".format(dirname, len(data.get()), actual, fp, ntotaltrails)










def parseCumulative(path):
    name = ""
    data = {}
    for line in open(path).readlines():
        if line[0] == "#":
            pass
        elif line[0].isalpha():
            name = line.strip()
            data[name] = {"val":[], "total":[], "actual":[], "fp":[], "exist":[]}
        if line[0].isdigit():
            val, total, actual, fp, exist = line.split(" ")
            data[name]["val"].append(float(val))
            data[name]["total"].append(float(total))
            data[name]["actual"].append(float(actual))
            data[name]["fp"].append(float(fp))
            data[name]["exist"].append(float(exist))
    return data

def normalize(data):
    normed = deepcopy(data)
    for key in data:
        for n in range(len(data[key]["total"])):
            normed[key]["actual"][n] /= data[key]["total"][n]
            normed[key]["fp"][n] /= data[key]["total"][n]
    return normed

def prepForPlot(data):
    d = deepcopy(data)
    for param in d:
        if param != "benchmark":
            w = abs(d[param]["val"][0]-d[param]["val"][1])/2.0
            shift = w/2.0
            d[param]["val"] = [x-shift for x in d[param]["val"]]
    return d

def plot2(data, normed, param):
    data = prepForPlot(data)
    normed = prepForPlot(normed)

    d = data[param]
    n = normed[param]

    f, axarr = plt.subplots(2, sharex=True)

    #these are fractions of positive detections
    #with respect to the total positive detections
    truedet = [(1-x)*100 for x in n["fp"]]

    w = abs(d["val"][0]-d["val"][1])/2.0
    ymin, ymax = min(truedet), max(truedet)
    h = abs(ymax-ymin)/10.0
    ymin, ymax = ymin-h, ymax+h

    axarr[0].bar(d["val"], d["total"], color="black", width=w,
                 label="Total number of positive detection")
    #axarr[0].bar(d["val"], d["fp"], color="red", width=w,
    #             label="False positives (frames not containing linear features)")
    #axarr[0].bar(d["val"], d["actual"], color="green", width=w,
    #             label="Frames containing actual linear features")

    axarr[1].bar(n["val"], [0,0,0,0], color="black", width=0,
                 label="Total number of positive detection")
    axarr[1].bar(n["val"], [100,100,100,100], color="darkgray", width=w,
                 label="False Positive Detections")
    axarr[1].bar(n["val"], truedet, color="dimgray", width=w,
                 label="True Positive Detections")
    

    axarr[1].set_ylim(ymin, ymax)
    axarr[0].set_ylim(0, max(d["total"])+max(d["total"])/10)

    axarr[0].set_title(param, {"fontsize":36})

    axarr[0].set_ylabel(r"$N_{frames}$", {"fontsize":42})
    axarr[1].set_ylabel("Fraction of \n Total Positive (%)", {"fontsize":32})
    axarr[1].set_xlabel("Parameter values", {"fontsize":32})
    
    #axarr[0].legend(bbox_to_anchor=(0.0, -0.15, 1., .102), loc=3, ncol=3,
    #                mode="expand", borderaxespad=0.)#, prop={"size":22})
    axarr[1].legend(bbox_to_anchor=(0.0, 1.03, 1.0, 0.102), loc=3, ncol=3,
                    mode="expand", borderaxespad=0.0, prop={"size":20})
    
    #axarr[1].legend()
    #f.set_tight_layout(True)

    plt.setp(axarr[0].get_yticklabels(), fontsize=20)
    plt.setp(axarr[1].get_xticklabels(), fontsize=20)
    plt.setp(axarr[1].get_yticklabels(), fontsize=20)
    
    axarr[0].grid()
    axarr[1].grid()




def plot(param):
    data = parseCumulative("/home/dino/Desktop/run_results/params_checks/removestars/false_positives/cumulative")
    normed = normalize(data)
    plot2(data, normed, param)
    plt.show()
