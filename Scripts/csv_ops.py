import csv
import os

class Operations():

    def __init__(self,path,rows):
        self.path = path
        self.rows = rows

    def createCSVFiles(self):
        with open(self.path,'w+',newline='') as fp:
            a = csv.writer(fp,delimiter=',')
            a.writerow(self.rows)

    def appendData(self):
        with open(self.path,'a+',newline='') as fp:
            a = csv.writer(fp,delimiter=',')
            a.writerows(self.rows)


class Deletefiles():
    
    def deleteFile(path='csv files'):
        for fp in os.listdir(path):
            if not fp.endswith(".csv"):
                continue
            os.remove(os.path.join(path,fp))