#
# Author: Rohith Bhaskaran <vrarohith@gmail.com>
#

import os
import tempfile

class StanfordParser:
    def __init__(self,working_dir=None):
        self.working_dir = working_dir
    
    def parse(self, sentence):
        in_file = self.makeFile(sentence)
        cmd = self.working_dir+'lexparser-typed.sh '+self.working_dir+' '+in_file+' >'+self.working_dir +'stanford_output.txt'
        os.system(cmd)
        out_file = open(self.working_dir+"stanford_output.txt")
        ret = out_file.read()
        os.remove(self.working_dir+'stanford_output.txt')
        os.remove(in_file)
        return ret

    def makeFile(self,sentence):
        input_file = tempfile.NamedTemporaryFile(prefix='stanford_input.txt',
                                                 dir=self.working_dir,
                                                 delete=False)
        input_file.write(sentence)
        input_file.write('\n')
        return input_file.name    
        
 
        