import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
#from sqlalchemy.pool import StaticPool #SqLite can't handle threading
                                       #when inmemory is used, this
                                       #is a "work-around"

import os


Base = declarative_base()

class Result(Base):
    __tablename__ = "result"
    
    run = sql.Column(sql.Integer, primary_key=True)
    camcol = sql.Column(sql.Integer, primary_key=True)
    filter = sql.Column(sql.String, primary_key=True)
    field = sql.Column(sql.Integer, primary_key=True)

    false_positive = sql.Column(sql.String, default=True)

    tai = sql.Column(sql.Float)

    crpix1 = sql.Column(sql.Float)
    crpix2 = sql.Column(sql.Float)

    crval1 = sql.Column(sql.Float)
    crval2 = sql.Column(sql.Float)

    cd11 = sql.Column(sql.Float)
    cd12 = sql.Column(sql.Float)
    cd21 = sql.Column(sql.Float)
    cd22 = sql.Column(sql.Float)

    x1 = sql.Column(sql.Float)
    y1 = sql.Column(sql.Float)
    x2 = sql.Column(sql.Float)
    y2 = sql.Column(sql.Float)

    image = sql.Column(sql.String)
    
    def __repr__(self):
        return ("<Result(run='{}', camcol='{}', filter='{}', "+\
               "field='{}'>").format(self.run, self.camcol,
                                     self.filter, self.field)


class Results(object):
    def __init__(self, respath=None, imgpath=None, alex=False):
        if os.path.isfile("/home/dino/Desktop/foo.db"):
            os.remove("/home/dino/Desktop/foo.db")
        self.engine = create_engine('sqlite:////home/dino/Desktop/foo.db',
        echo=False)
        #self.engine = create_engine("sqlite:///:memory:", echo=False)
#                                    connect_args={'check_same_thread':False},
#                                    poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()

        self.alex = alex
        self.keys = Result.metadata.tables["result"].columns.keys()
        
        if respath:
            self.respath = self.expandpath(respath)
            self.initResults()
        if imgpath:
            self.imgpath = self.expandpath(imgpath)
            self.initImages()



    def expandpath(self, path):
        if path[0] == "~":
            path = os.path.expanduser(path)
        if os.path.exists(path):
            return path
        else:
            raise IOError("Sent path "+path+" does not exist.")

    def initResults(self):
        if os.path.isfile(self.respath):
            self.readFile(self.respath)
        else:
            filelist = self.__getFilesByCriteria(self.respath,
                                             lambda x: x=="results.txt")
            print len(filelist)
            for filename in filelist:
                self.readFile(filename)
        self.session.commit()

    def readFile(self, f):
        if type(f) == str:
            f = self.expandpath(f)
            f = open(f)
        if type(f) == file:
            for line in f.readlines():
                if self.alex:
                    parsed = self.__parseStringAlex(line)        ####MONKEYPATCHED; FIX IT LATER!
                else:
                    parsed = self.__parseString(line)
                res = Result(**parsed)
                self.session.add(res)
        else:
            raise IOError("Send a path to an existing file or a file."+\
                          "Got "+type(f)+" instead")
            

    def __getFilesByCriteria(self, path, criterion):
        filelist = list()
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if criterion(filename):
                    filelist.append(os.path.join(dirpath, filename))
        if len(filelist) == 0:
            raise IOError("No desired files found in the folder "+\
                          "path provided.")        
        return filelist

    def __parseStringAlex(self, string):
        s = string.split(" ")
        fr = s[0].split("-")                     #boze alex wtf ti je sa frameovima
        parsed = {"run":int(fr[2]), "field":int(fr[4][:4]), "camcol":int(fr[3]), "filter":fr[1],
                "tai":float(s[6]), "crpix1":float(s[7]), "crpix2":float(s[8]), "crval1":float(s[9]),
                "crval2":float(s[10]), "cd11":float(s[11]), "cd12":float(s[12]), "cd21":float(s[13]),
                "cd22":float(s[14]), "x1":float(s[17]), "y1":float(s[18]), "x2":float(s[19]), "y2":float(s[20])}
        return parsed


    def __parseString(self, string):
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


    def initImages(self):
        allimg = self.__getFilesByCriteria(self.imgpath,
                                           lambda x: x[-3:]=="png")
        for img in allimg:
            frame = self.getFrameFromImgPath(img) #HANDLE THE ERRORS!!!! ASAP!!!
            try:
                self.update({"image":img}, **frame)
            except:
                pass

    def getFrameFromImgPath(self, imgpath):
        tail = os.path.split(imgpath)[-1] # get just filename+extension
        imgname = os.path.splitext(tail)[0] # get just filename
        frame, filter, run, camcol, field = imgname.split("-")  ### THIS IS VERY SDSS ORIENTED?!
        field = field.split(".")[0]
        return {"filter":filter, "run": int(run),
                "camcol": int(camcol), "field": int(field)}

    def update(self, what, **kwargs):
        query = self.session.query(Result)
        res = query.filter_by(**kwargs).all()
        if len(res) == 0:
            raise sql.exc.ArgumentError("No matching Result found. "+\
                                        "Invalid frame specifiers.")
        elif len(res) == 1:
            for key in what:
                setattr(res[0], key, what[key])
        else:
            raise AttributeError("List has no attribute "
                                 + what.keys()[0])
        self.session.commit()
        

    def get(self, columns=None, **values):
        if columns is None:
            query = self.session.query(Result)
        else:
            attrs = [getattr(Result, x) for x in columns]
            query = self.session.query(*attrs)
        execute = query.filter_by(**values)
        return execute.all()
