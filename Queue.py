from ytd import *
class Queue:
    def __init__(self):
        self.current=None
        self.lista=[]
        self.currname=None
        self.next=None

    async def updateplay(self,loop):
        if self.lista:
            self.current=self.lista.pop(0)
        else:
            self.current=None
            print("xd")
        if self.next is not None:
            self.currname=self.next
        else:
            self.currname=await YTDLSource.from_url(self.current,loop=loop)
    async def downnex(self,loop):
        if self.lista:
            self.next=await YTDLSource.from_url(self.lista[0],loop=loop)

    def list(self):
        temp=''
        temp+="Obecnie grane jest {}\n".format(self.current)
        temp+="W kolejce jest\n"
        for a in self.lista:
            temp+=a+"\n"
        return temp

    def add(self,song):
        self.lista.append(song)
    
    def remove(self,i):
        if int(i)==0:
            self.next=None
        del self.lista[int(i)]
                
        

