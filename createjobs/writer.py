"""
Writer functions that writes the actual dqs files.

  Functions
---------------
writeDqs - writes the QSUB dqs files witht he params from a Job object.
"""

import os


def writeDqs(job, runlst):
    """
    Writes the job#.dqs files. Takes in a Jobs instance and processes the
    "generic" template replacing any/all keywords using values from Jobs instance.
    
    For each entry in runlst it creates a new job#.dqs file, which contains
    commands to execute detecttrails processing for each entry of entry in runlst.
    """
    for i in range(0, len(runlst)):
        jobpath = os.path.abspath(job.save_path)
        newjobpath = os.path.join(jobpath, "job"+str(i)+".dqs")
        newjob = open(newjobpath, "w")
        temp = open(job.template_path).read()

        temp = temp.replace("JOBNAME", str(runlst[i][0])
                            +"-"+str(runlst[i][-1]))
        temp = temp.replace("QUEUE", job.queue)
        temp = temp.replace("WALLCLOCK", job.wallclock)
        temp = temp.replace("PPN", job.ppn)
        temp = temp.replace("CPUTIME", job.cputime)

        header = temp.split("COMMAND")[0]
        footer = temp.split("COMMAND")[1]

        for x in runlst[i]:
            if job.pick.lower() in ["run", "runs", "fromruns"]:
                header+=job.command.replace("$", "run="+str(x))

            if job.pick.lower() in ["runfilter", "filterrun", "fromrunfilter"]:
                header+=job.command.replace("$", "run="+str(x) +
                                               ", filter='"+str(job.filter)+"'")
            if job.pick.lower() in ["runcamcol", "runcamcol", "fromruncamcol"]:
                header+=job.command.replace("$", "run="+str(x) +
                                                ",camcol=" +str(job.camcol))
            if job.pick.lower() in ["runfiltercamcol", "runcamcolfilter", 
                                "fromruncamcolfilter", "fromrunfiltercamcol"]:
                header+=job.command.replace("$", "run="+str(x) +
                                                ",camcol=" +str(job.camcol) +
                                                ",filter='"+str(job.filter)+"'")


            header = header.replace("NODEFLAG", "1")
            header = header.replace("FERMINODE", "fermi-node01")
            
        newjob.writelines(header+footer)

    newjob.close()

__author__ = "Dino Bektesevic"
__copyright__ = "Copyright 2017, Linear Feature Detection Algorithm (LFDA)"
__credits__ = ["Dino Bektesevic"]
__license__ = "GPL3"
__version__ = "1.0.1"
__maintainer__ = "Dino Bektesevic"
__email__ = "dino@iszd.hr"
__status__ = "Development"