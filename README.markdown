Computer vision algorithms are powerful tools in astronomical image analyses, especially when automation of object detection and extraction is required. Modern object detection algorithms in astronomy are oriented towards detection of stars and galaxies, ignoring completely detection of existing linear features. With the emergence of wide-field sky surveys, linear features attract scientific interest as possible trails of fast flybys of near-Earth asteroids and meteors. In this work we describe a new linear feature detection algorithm designed specifically for implementation in Big Data astronomy. The algorithm combines a series of algorithmic steps that first remove other objects (stars, galaxies) from the image and then enhance the line to enable more efficient line detection with the Hough algorithm. The rate of false positives is greatly reduced thanks to a step that replaces possible line segments with rectangles and then compares lines fitted to the rectangles with the lines obtained directly from the image. The speed of the algorithm and its applicability in astronomical surveys are also discussed. 

# Installation

There is no specific installation required. The code requires sevaral libraries and modules some of which are bundled with the code and is not Python 3 compatible. To read in more details on how the processing is done see: https://arxiv.org/abs/1612.04748

As the code is currently actively under development it is subject to change without notification.

### Requirements:

* Python 2.7
* OpenCV 2.4.9
* NumPy 1.12.1
* Fitsio 0.9.7

# Running the code

Currently LFDA is setup to work with SDSS folder structure and files. The data has to be accessible and in the same format and file structure as is availible from SDSS SAS servers. To see how to access the SDSS data read: http://www.sdss.org/dr12/data_access/tools/

The expected folder structure and availible files are:
* boss
  * photo
    * redux
        * photoRunAll-dr[xy].par
        * runlist.par
  * photoObj
    * 301
      * [run]
        * [camcol]
          * photoObj-[run]-[camcol]-[field].fits
    * frames
      * 301
        * [run]
          * [camcol]
            *frame-[filter]-[run]-[camcol]-[frame].fits.bz2

Where the [designations] mark the alphanumerical values that identify specific SDSS data.

There is an additional fitsdmp folder to which the images are bunzipped and deleted after processing. 

To locate and navigate through the folder structure LFDA uses environmental variables and files `photoRunAll-dr[xy].par` and `runlist.par`. These files can be data release specific and are availible from SDSS SAS servers. 

Edit the start.sh environmental BOSS variable to point to the folder with SDSS data. Additionally edit the FITSDMP environmental variable to point to the folder where you would like the fits to be unpacked to. One is provided withing the LFDA folder but it's not mandatory to use it. Invoke start.sh to run LFDA. An python 2.6 IDLE will open with the commands availible but LFDA can be run in other modes as well. Feel free to edit start.sh to match your requirements.

# DetectTrails module

This modules task is to process images. To import it do either:

```python
import detecttrails
import detectrails as dt
```

The class that starts and controls the execution is called DetectTrails. It is a convenience class that holds various execution parameters and processes SDSS fields that can also be selected in batches by their identifications. Simple usage would be:

```python
foo = DetectTrails(run=2888)
foo = DetectTrails(run=2888, camcol=1)
foo = DetectTrails(run=2888, camcol=1, filter='i')
foo = DetectTrails(run=2888, camcol=1, filter='i', field=139)
```

It is possible to change detection/execution parameters of class object by:

```python
foo.params_bright["debug"] = True
foo.params_removestars["filter_caps"]["i"] = 20 
```

See the `DetectTrails` class help string, `detecttrails` module help string or the paper linked at the top for full list of execution/detection parameters and their explanation.

Results are outputted to a file provided by the filepath `results`. By default it is set to `results.txt`. Results file is a CSV file in which the detected parameters, if a line is found, are stored in the following order:

```run field camcol filter tai crpix1 crpix2 crval1 crval2 cd1_1 cd1_2 cd2_1 cd2_2 x1 x2 y1 y2```

All errors are forcefully silenced. This is done not to interrupt an entire batch processing session because of a corrupt file or a bug. Errors are logged in a file `errors`, defaultly set to `errors.txt`. Each error is a 3 stack deep traceback printed in the following format:                

```
run,camcol,field,filter
TRACEBACK (3 stacks deep)
Error message of 1st stack.
```

#### Debug mode

A special mode in which this class can operate is the debug mode that can be selected by:

```python
foo.params_bright["debug"] = True
```

In this mode all the test values like `linesetTresh`, `thetaTresh`, `dro` etc. are printed to the standard out. Additionally a set of images displaying the processing steps are saved in the home folder of the LFDA. To find out more about the meaning read the paper linked in the Installation section. Following images are saved:
                    
1. equBRIGHT - equalized image for BRIGHT 
2. contoursBRIGHT - drawn minAreaRect that pass the lw tests for BRIGHT
3. equhoughBRIGHT - nlinesInSet hough lines drawn on 1)
4. boxhoughBRIGHT - nlinesInSet hough lines on 2)
5. equDIM - equalized image for DIM
6. erodedDIM - eroded 5)
7. openedDIM - dilated 6)
8. contoursDIM - drawn minAreaRect that pass the lw tests for DIM
9.  equhoughDIM - nlinesInSet hough lines drawn on 7
10. boxhoughDIM - nlinesInSet hough lines drawn on 8


In detecttrails module a function `process_field` is invoked that handles the unpacking, reading, processing and outputting of the results for every frame. It is possible to invoke this function directly, however very inconvenient.

```python
process_field(results, errors, run, camcol, filter, field, params_bright, params_dim)
```
  
# Createjobs module

Createjobs module is used to create .dqs files necessary to run a job on QSUB system. Main idea was to create a class that can take care of writing a large job requests on users behalf without the need to always edit the template through terminal or writing specific jobs by hand. To access this module functionality import it in one of the following ways:

```python
import createjobs
import createjobs as cj
from createjobs import Jobs
```

By default the opened template is called `generic` and can be found in the same folder this module resides in. Since it's neccesary to change a lot of parameters, especially paths, template can be edited, or a new one can be sent in its place. Specifying template_path at class instantiation time will instruct writer to change that template. When writing your own template, to avoid error reports, you have to specify all parameters in the new template that this class can change. Parameters are uppercase single words, i.e: JOBNAME, QUEUE, NODEFLAG

All environmental paths, such as where the data is located or where the results and errors should be saved, in the template are NOT changable throught this class. Edit them directly, f.e. the save path for results is given by: 

```bash
cp *.txt /home/fermi/$user/run_results/$JOB_ID/
```

The module is highly flexible and can be easily adapted to fit various different execution environments. It has several different usage cases depending to enable very high execution specification. 

### Simple use case

The simplest one is just specifying the number of jobs you want. Jobs will then take all the runs found in runlist.par file with rerun 301 and create jobs to process them. Be carefull about processing too many runs in a single job because WALLCLOCK or CPUTIME can expire.

```python
>>> jobs = cj.Jobs(500)
>>> jobs.create()
    There are no runs to create jobs from.
    Creating jobs for all runs in runlist.par file.
	  
    Creating: 
        765 jobs with 1 runs per job 
	Queue:     standard 
	Wallclock: 24:00:00 
	Cputime:   48:00:00 
	Ppn:       3 
	Path:      /home/user/Desktop/.../jobs
```

User will be notified about all important parameters that were set. Notice that the save path, queue, wallclock, ppn and cputime are set by default. Also notice that we specified 500 jobs to be created but 765 jobs were created. This is intentional. Jobs looks for the next larger whole number divisor divisor to split the jobs between.

### Specifying runs

Specifying certain runs by hand is possible by sending a list of runs of interes:

```python	
>>> runs = [125, 99, 2888, 1447]
>>> jobs = cj.Jobs(2, runs=runs)
>>> jobs.create()
    Creating: 
        2 jobs with 2 runs per job 
        Queue:     standard 
        Wallclock: 24:00:00 
        Cputime:   48:00:00
            Ppn:       3
            Path:      /home/user/Desktop/.../jobs
```

### Selecting processing data

Specifying aditional keyword arguments to Jobs class helps you utilize DetectTrails class run options. Sent kwargs are applied globaly across every job. It's not possible to specify separate kwargs for each job. 

```python
>>> runs = [125, 99, 2888, 1447]
>>> jobs = cj.Jobs(2, runs=runs, camcol=1)
>>> jobs.create()

 would create 2 jobs with 2 runs per job as the above example. But the actuall call to DetectTrails class would now look like:

```bash     
python -c "import detect_trails as dt;
           dt.DetectTrails(run=125,camcol=1).process()"
```
     
Which would process only the camcol 1 of run 125. Actual written job#.dqs file is not as readable/friendly as above examples. Another example:

```python
>>> jobs = cj.Jobs(2, runs=runs, camcol=1, filter="i")
```

would execute 2 jobs with following 2 calls to DetectTrails class:

```python
python -c "import detect_trails as dt; 
           dt.DetectTrails(run=125,camcol=1,filter=i).process()"
```

See help on DetectTrails class for a list of all options.

### Specifying detection parameters

To further fine tune your job behaviour it's possible to change the default execution command to supply additional execution parameters. By default, the keyword argument `command` is set to:

```python
python -c "import detecttrails as dt;
           dt.DetectTrails($).process()"
```

Where "$" sign gets automatically expanded by the writer module. There should ALWAYS be a "$" character present in a command. "$" replaces arguments of DetectTrails class at instantiation, sort of as **kwargs usually do. Example:

```python
>>> jobs = cj.Jobs(2, runs=runs, camcol=1, filter="i")
>>> jobs.command = 'python -c "import detecttrails as dt;' +\
                   'x = dt.DetectTrails($);'               +\
                   'x.params_bright[\'debug\'] = True;'    +\
                   'x.process()"\n'
>>> jobs.create()
```

which will be written as:

```bash
python -c "import detecttrails as dt;
           x = dt.DetectTrails(run=125,camcol=1,filter=i);
           x.params_bright['debug'] = True;
           x.process()"
```

Again, the actual written command in the job#.dqs file would not look as user friendly as here. In the above example notice that quotation-marks are trice nested as follows:

```
'    ("  (\'  \')   ")    '
```

This complication is here because the command has to be sent as a string therefore the quotation marks used inside should not escape the outsidemost quotations. Outtermost declare a python string which becomes the command attribute of Jobs class. Inner double quotations enclose the string that will be executed by `python -c` command. Innermost escaped single quotations designate a string that will be interpreted as an argument to the DetectTrails parameters. General usefull guidelines:
1. the outter-most quotation as single '' marks
2. everything past "-c" flag in double quotation marks ""
3. further quotation marks should be escaped single quotations.
4. a EXPLICIT newline character should ALWAYS be at the end.    

To see all availible parameters and arguments to the Jobs class see its help string. 

# License

Copyright (C) 2017  Dino Bektesevic

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


