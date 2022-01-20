import yaml
import os
from application_logging.logger import AppLog
import pandas as pd

def read_config(config_path):
    with open(config_path) as config_file:
        content = yaml.safe_load(config_file)

    return content


class FileOperations:

    def __init__(self,execType='Training'):
        self.execType = execType
        self.applog = AppLog(self.execType)
        self.log = self.applog.log("sLogger")

    def IsFileAvailable(self, filename=None):

        try:
            FileAvailable = 1
            if filename == None:
                self.log.info("File Name is missing as Input argument :")
                FileAvailable = 0
            else:
                if not os.path.isfile(filename):
                    self.log.info("File Name is not available in given path :")
                    FileAvailable = 0

        except Exception as e:
            self.log.critical('Exception occured, while validating the file availability : {}'.format(e))

        return FileAvailable

    def IsDirectoryAvailable(self, dir=None):

        try:
            DirectoryAvailable = 1
            #print("Checking the available directory path : {}".format(dir))
            if dir == None:
                self.log.info("Directory path is missing as Input argument :")
                DirectoryAvailable = 0
            else:
                if not os.path.exists(dir):
                    self.log.info("Directory is not available in given path : {}".format(dir))
                    DirectoryAvailable = 0

        except Exception as e:
            self.log.critical('Exception occured, while validating the file directory availability : '.format(e))

        return DirectoryAvailable

    def ReadCSVData(self,filepath=None, Separator=',', skiprows=0, columns=None):

        try:
            Data = pd.DataFrame()
            Status = 0
            if filepath != None:
                DirName, FileName = os.path.split(filepath)

                if self.IsDirectoryAvailable(DirName) == 1:

                    filepath = DirName + '\\'+ FileName
                    self.log.info('File path to read file : {}'.format(filepath))

                    if self.IsFileAvailable(filepath) == 1:
                        if columns == None:
                            Data = pd.read_csv(filepath,sep=Separator, skiprows=skiprows, low_memory=False)
                        else:

                            Data = pd.read_csv(filepath,sep=Separator, skiprows=skiprows, names=columns, low_memory=False)
                            #Data = Data.astype(DataType)
                            #print("Data type for the Data is : ",type(Data))

                        Status = 1
        except Exception as e:
            self.log.critical("Exception occured, while reading the data from file {}: ".format(e))

        return Status, Data