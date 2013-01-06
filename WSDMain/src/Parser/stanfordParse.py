import os,sys
import os
cmd1 = '/home/anu/stanford-parser-2012-11-12/lexparser.sh /home/anu/stanford-parser-2012-11-12/data/testsent.txt > output.txt'
os.system(cmd1)

fil=open('output.txt') 
temp=fil.read().split('\n\n')

dependency=[] #List containing dependencies
for i in range(1,len(temp)-1,2):
    dependency.append(temp[i])
fil.close()

fil=open('output.txt','w') #Writing the dependecy to fil: output.txt
for d in dependency:
    print d+'\n'
    fil.write(d+'\n')
fil.close()