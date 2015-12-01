#-*- coding:gb2312 -*-


from glob import glob
from collections import defaultdict
import os

from mybio.combat import combat
from mybio.enrich import analysis

def write(data,file = None):
    if not file:
        import datetime
        file = 'Result(%s).txt'%datetime.datetime.now().strftime('%H%M%S')
    if '\\' in file:
        d, name = os.path.split(file)
        try:
            os.makedirs(d)
        except:
            pass
        print('%s saved to dir(%s)!'%(name, d))
    else:
        print('%s saved to current dir!'%file)    
    with open(file, 'w') as da:
        da.writelines(data)     

class Esdata():

    def __init__(self, file, tarindex = None, sep='\t'):
    
        self.name = os.path.basename(file)
        self.pdict = {n.split('\t')[0]:n for n in open(file)}
        self.gdict = defaultdict(list)
        self.head = self.pdict['ProbeName']
        if not tarindex:
            line = self.head.strip().split('\t')
            numi = [n for n in line if 'Gene' in n]
            if len(numi) == 1:
                tarindex = line.index(numi[0])
            else:
                print(numi)
                tarindex = line.index(numi[0])
        for probe in self.pdict:
            line = self.pdict[probe].split('\t')
            pid,tarid = line[0],line[tarindex].strip()
            if tarid:
                self.gdict[tarid].append(pid)
                
    def get(self,tarid):
    
        res = self.gdict.get(tarid.strip())
        if res:
            return [self.pdict.get(pid) for pid in res]
        else:
            print('NOTE:The %s can"t find in %s!'%(tarid, self.name))
            return []
    
    @staticmethod
    def gene(self):
        return self.gdict.keys()

def getfile(m):
#m is search pattern.Example:search some file include 'mRNA',
#Then the pa is mRNA. pa should not in the boundary!
    pa = '*%s*'%m
    files = glob(pa)
    print(files)
    if len(files) == 1:
        return files[0]
    elif len(files) > 1:
        return files
    else:
        raise SearchFileError
    
