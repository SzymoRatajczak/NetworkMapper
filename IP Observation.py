import pickle
import datetime
class IPObservationDictionary:
    def __init__(self):
        self.Dictionary={}

    def AddObj(self,object):
        now=datetime.datetime.now()
        houre=now.hour
        if object in self.Dictionary:
            curValue=self.Dictionary[object]
            curValue[houre-1]=curValue[houre-1]+1
            self.Dictionary[object]=curValue
        else:
            curValue=[0,0,0,0,0,0,0,0,0]
            curValue[houre-1]=curValue[houre-1]+1
            self.Dictionary[object]=curValue


    def SaveObj(self,file):
        file=open(file,"w")
        pickle.dumps(self.Dictionary,file)


    def LoadObj(self,file):
        file=open(file,"r")
        self.Dictionary=pickle.loads(file.read())

    def getObj(self,object):
        if object in self.Dictionary:
            print(object)
        else:
            print("Object does not exist")


    def __del__(self):
        print("Closed")


ip=IPObservationDictionary()
ip.AddObj("192.168.0.1","129.187.0.29",80)
ip.AddObj("192.168.0.1","129.187.0.29",80)
ip.AddObj("192.168.0.1","129.187.0.29",80)
ip.AddObj("192.168.0.1","129.187.0.29",80)
ip.AddObj("192.168.0.1","129.187.0.29",80)

value=ip.GetObj("192.168.0.1","129.187.0.29",80)
print("your value:"+ value)

ip.SaveObj("dumplist.dict")

ip.LoadObj("dumpList.dict")


