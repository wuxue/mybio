#-*- coding:gb2312 -*-

import os
try:
    import cPickle as pickle
except ImportError:
    import pickle
from collections import defaultdict


path = r'E:\Scripts\mypackages\mybio\data\BIOGRID'
f1 = 'BIOGRID-ALL-3.4.127.tab2.txt'



class Network():
    
    def __init__(self, org):
        self.org = str(org)
        self.name = '%s\%s_%s.pkl' % (path, f1[:-4], self.org)
        if os.path.isfile(self.name):
            print(self.name)
            ff = open(self.name, 'rb')
            self.data = pickle.load(ff)
            ff.close()
        else:
            self.data = self._parse()        
    
    def _parse(self):
        file = os.path.join(path, f1)
        temp = defaultdict(list)
        head, *data = open(file)
        for line in data:
            nl = line.split('\t')
            if nl[15] == nl[16] == self.org:
                temp[(nl[1], nl[2])].append(line)
        temp['head'] = head
        with open(self.name, 'wb') as fd:
            pickle.dump(temp, fd)
        return temp
        
    def query(self, geneids, name=None):
        '''
        Please input the GeneID!'''
        pairgs = []
        for i in geneids:
            for j in geneids:
                if i != j:
                    pairgs.append((i, j))
                    pairgs.append((j, i))
        res = []
        for pair in pairgs:
            tar = self.data.get(pair)
            if tar:
                res += tar
        res.insert(0, self.data['head'])
        name = name if name else 'Network_result'        
        with open(name + '.txt', 'w') as fd:
            fd.writelines(res)
        return geneids
        