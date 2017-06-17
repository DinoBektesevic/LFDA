import os
import re
import csv
import createjobs
import inspect

qsub = r"/home/dino/Desktop/jobs3/"
dettrails = r"/home/dino/Desktop/run_results3/"
f = r"/home/dino/Desktop/test.txt"
#pathres = r"/home/dino/Desktop/res/res"
#alex = r"/home/dino/Desktop/jobs/allhits.txt"
#alextest = r"/home/dino/Desktop/jobs/allhits_test.txt"

class QsubErr:
    """
    Class that contains all errors read form a Qsub outputs.
    
    init parameters
    ----------------
    Keywords:
    
        path:
            path to catenated file of all output errors.
            It will look only for files of *-*.e* nametype.

      methods
    -----------
    errexists(filename, jobid):
        returns True or False. Noerror state is defined if only
        self.noerrors is found in a *-*.e* qsub file.
    getall():
        returns a list( dict() ) or all the errors. Each dict()
        contains RunID ("startrun-endrun"), JobID and the error (Err)
        in question.
    """        

    def __init__(self, path):
        self.path=path
        self._templine=""
        self.noerror = 196 #bytesize of fermi files without an error
        self.errors = self.read()


    def errExists(self, filename):
        path = os.path.join(self.path, filename)
        if (os.path.getsize(path) != self.noerror):
            return True
        return False

    def getError(self, filename, jobid):
        file = open(os.path.join(self.path, filename))
        noerror = ["/var/spool/torque/mom_priv/jobs/JOBID.fermi.SC[49]: .[5]: .[44]: shopt: not found [No such file or directory]",
                   "/var/spool/torque/mom_priv/jobs/JOBID.fermi.SC[49]: .[5]: .[63]: [: argument expected"]
        noerror1 = noerror[0].replace("JOBID", str(jobid))
        noerror2 = noerror[1].replace("JOBID", str(jobid))
        #print (noerror1, noerror2)
        #print(self.noerror)
        for line in file.readlines():
            errline = ""
            if line.strip() not in (noerror1, noerror2):
                errline += line.strip()
        return errline
        
                    
    def read(self):
        p = re.compile("\d*-\d*.e\d*")
        errors = list( dict() )
        for filename in os.listdir(self.path):
            if(p.match(filename)):
                runid = filename.split(".")[0]
                jobid = filename.split(".")[1][1:]
                if(self.errExists(filename)):                    
                    errors.append({"RunID":runid,
                                   "Err":self.getError(filename, jobid),
                                   "JobID":jobid})
        return errors    


class DetectTrailsLogs:
    """
    Class that contains all errors read form detecttrails outputs.
        
    init parameters
    ----------------
    Keywords:
    
        path:
            path results folder structure.
            Will only read in files named errors.txt.

      methods
    -----------
    getall():
        returns a list( dict() ) or all the errors. Each dict()
        contains run, camocl, field, filter, error in question
    """ 

    def __init__(self, path):
        self.path=path
        self._runid = ""
        self._camcol=""
        self._field=""
        self._filter=""
        self._error=""
        self.errors = self.read()

    def _getFiles(self):
        filelist = list()
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            for filename in filenames:
                if filename == 'errors.txt':
                    filelist.append(os.path.join(dirpath, filename))
        return filelist

    def read(self):
        p = re.compile("\d*,\w")
        p1 = re.compile("ValueError:")
        errors = list( dict() )
        for filename in self._getFiles():
            file = open(filename)
            for line in file.readlines():
                errexists = False
                if(p.match(line)):
                    self._runid=line.split(",")[0]
                    self._camcol=line.split(",")[1]
                    self._field=line.split(",")[2]
                    self._filter=line.split(",")[3].strip()
                if (p1.match(line)):
                    self._error = line.strip()
                    errexists = True
                if(errexists):
                    errors.append({"Run":self._runid,"camcol":self._camcol,
                                    "filter":self._filter,"field":self._field,
                                    "Err":self._error})
        return errors
            

    def getAll2(self):
        file = open(self.path)
        p = re.compile("\d*,\w")
        p1 = re.compile("ValueError:")
        for line in file.readlines():
            errexists = False
            if(p.match(line)):
                self.__runid=line.split(",")[0]
                self._camcol=line.split(",")[1]
                self._field=line.split(",")[2]
                self._filter=line.split(",")[3].strip()
            if (p1.match(line)):
                self._error = line.strip()
                errexists = True
            if(errexists):
                self.errors.append({"Run":self.runid,"camcol":self.camcol,
                                "filter":self.filter,"field":self.field,
                                "Err":self.error})
        return self.errors  

class Errors:
    """
    Class that contains all errors read (Qsub+detecttrails logs).
    Parse all errors with this class.    
    
    init parameters
    ----------------
    Keywords:
    
        path:
            path to folder with all qsub errors
        pathlog:
            path to folder with all detectrails errors

      methods
    -----------
    toFile(filename):
        prints out all errors found into a new file given by filename.
        Errors are sorted, each run is printed under the runID and JobID
        in which it executed. ****DOESN'T REALLY WORK WELL!****
    """ 
    def __init__(self, qsubErrpath, dettrailsErrpath):
        self.qsub = QsubErr(qsubErrpath).errors
        self.dettrails = DetectTrailsLogs(dettrailsErrpath).errors

    def toFile(self, filepath):
        file = open(filepath, "w")
        for qerr in self.qsub:
            bot = int(qerr["RunID"].split("-")[0])
            top = int(qerr["RunID"].split("-")[1])
            #print(bot, top, int(logs[0]["Run"]))
            file.writelines(qerr["RunID"]+" "+qerr["JobID"]+" "+qerr["Err"]+"\n")
            for lerr in self.dettrails:
                if (bot <= int(lerr["Run"]) and top>=int(lerr["Run"])):
                    file.writelines(("    {} {} {} {} {}\n").format(lerr["Run"], lerr["camcol"],
                                                        lerr["filter"], lerr["field"], lerr["Err"]))
        file.close()

    def _removeDuplicates(self, runs, fun=None):
        seen = set()
        return [ x for x in runs if not (x in seen or seen.add(x))]

    def _genRunsQsub(self):
        runs = list()
        for qerr in self.qsub:
            top = int(qerr["RunID"].split("-")[1])
            bot = int(qerr["RunID"].split("-")[0])
            if (top!=bot):  runs.extend([x for x in range(bot, top)])
            else: runs.append(bot)
        return runs

    def _genRunsDT(self):
        allerr = list()
        for lerr in self.dettrails:
            allerr.append(lerr["Run"])
        runs = self._removeDuplicates(allerr)
        return runs

    def genJobsQsub(self, kwargs=None):
        runs = self._genRunsQsub()
        if kwargs:
            self.jobs = createjobs.Jobs(len(runs),runs=runs, **kwargs)
        else:
            self.jobs = createjobs.Jobs(len(runs), runs=runs)

        self.jobs.create()

    def __len__(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, context=15)
        for i in range(5):
            print "    caller: ",calframe[i][3]
        len1 = len(self.qsub)
        print "Number of failed QSUB jobs: ", len1
        len2 = len(self.dettrails)
        print "Number of failed frames (DetTrails errors): ", len2
        print "Total errors occured QSUB+DetTrails = "
        return len1+len2













        
        
