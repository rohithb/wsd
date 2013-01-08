#@PydevCodeAnalysisIgnore
import os,sys
import os

class StanParse:
    def __init__(self):
        self.workingdir =   "/home/anu/stanford-parser-2012-11-12/"
        self.cmd = self.workingdir+"lexparser.sh "+self.workingdir+"infile.txt > " +self.workingdir+"outfile.txt"
    
    def makeInFile(self, request):
        fil=open(self.workingdir+'infile.txt','w')
        fil.write(request)
        fil.close()
        
    def parse(self):
        
        os.system(self.cmd)
        #os.remove(self.workingdir+'infile.txt')
        
        fil=open(self.workingdir+'outfile.txt','r')
        temp=fil.read().split('\n\n')
        
        dependency=[] #List containing dependencies
        for i in range(1,len(temp)-1,2):
            dependency.append(temp[i])
        fil.close()
        
        for i in range(1,len(dependency)):
            return dependecy[i]
        
        
