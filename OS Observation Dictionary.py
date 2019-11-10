import pickle
import datetime

class OSObservationDictionary:
    def __init__(self):
        self.Dictionary={}

    def AddObj(self,object):
        time=datetime.datetime.now()
        hour=time.hour
        if object in self.Dictionary:
            current=self.Dictionary[object]
            current[hour-1]=current[hour-1]+1
            self.Dictionary[object]=current
        else:
            current=[0,0,0,0,0,0]
            current[hour-1]=current[hour-1]+1
            self.Dictionary[object]=current

    def GetObj(self,object):
        if object in self.Dictionary:
            print("your object:",object)
        else:
            print("Object does not exist")

    def SaveObj(self,file):
        try:
            file_open=open(file,'w')
            pickle.dumps(self.Dictionary,file_open)
            file_open.close()
        except:
            print("Cannot dump a file ")
    def LoadObj(self,file):
        try:
            file_open=open(file,"r")
            self.Dictionary=pickle.loads(file_open.read())
            file_open.close()
        except:
            print("Loading failed")

    def __del__(self):
        print("all closed")


def main():
    ip=OSObservationDictionary()
    ip.AddObj("192.168.0.1", "129.187.0.29", 80)
    ip.AddObj("192.168.0.1", "129.187.0.29", 80)
    ip.AddObj("192.168.0.1", "129.187.0.29", 80)
    ip.AddObj("192.168.0.1", "129.187.0.29", 80)
    print(ip.GetObj("192.168.0.1","129.187.0.29",80))
    ip.SaveObj("myfile.dict")
    ip.LoadObj("myfile.dict")

