from glob import glob
import os
import pandas as pd
from collections import defaultdict


def readterm(file):

    tarcolumns = [1, 5, 6, 7, 8]
    res = []
    for line in open(file):
        line = line.split('\t')
        if line[1] == 'PROBE':
            line[1] = 'GeneSymbol'

        newline = [line[i] for i in tarcolumns]
        res.append('\t'.join(newline) + '\n')
    with open(file, 'w') as data:
        data.writelines(res)
class Report():
    
    
    def __init__(self, file):
        self.name = file.split('_')[3]
        self.df = pd.read_table(file, index_col=0)
        self.term = self.df.index
        self.getf()
        self.creat()
    def getf(self):
        files = glob('*')
        self.fs = defaultdict(list)
        for file in files:
            for key in self.term:
                if key in file:           
                    self.fs[key].append(file)
    def creat(self):
        self.pa = {}
        try:
            os.mkdir(self.name)
        except FileExistsError:pass
        dirr = {'2_TermDetail':'xls', '1_EnrichmentPlot':'enplot', '3_Heatmap':'other'}
        for name, value in dirr.items():
            pa = os.path.join(self.name , name)
            try:os.mkdir(pa)
            except FileExistsError:pass
            self.pa[value] = pa

    def save(self):
        self.df = self.df.ix[:,2:]
        self.df.to_csv(r'%s\GSEA_Report_fo_%s.txt' % (self.name, self.name), sep='\t')
        for i, term in enumerate(self.df.index):
            i += 1
            termfilelist = self.fs[term]
            for termfile in termfilelist:
                newname = '%d_%s' % (i, termfile)
                if termfile.endswith('xls'):
                    readterm(termfile)
                    newpa = os.path.join(self.pa['xls'], newname)                    
                elif termfile.startswith('enplot'):
                    newpa = os.path.join(self.pa['enplot'], newname)
                else:
                    newpa = os.path.join(self.pa['other'], newname)
                os.rename(termfile, newpa)
                print(termfile, '--->', newpa)
                
                
for report in glob('gsea_report_for*.xls'):
    a = Report(report)
    a.save()
