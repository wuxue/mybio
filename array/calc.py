from collections import defaultdict

import pandas as pd

class Data:
    def __init__(self, file=None, groupfile=None, platform=None, samplefile=None):
        self._filename = file
        self._groupsfile = groupfile
        self._platform = platform
        self._samples = samplefile

    def feed(self, file, groupfile, samplefile=None):
        self._groupsfile = groupfile
        self._samples = samplefile
        self._filename = file

    def parsegroup(self, sep=','):
        self._group = defaultdict(list)
        for line in open(self._groupsfile):
            gname, treats, controls = line.strip().split('\t')
            self._group[gname].append((treats.split(sep), controls.split(sep)))

    def parsedata(self):
        self.data = pd.read_table(self._filename, index_col=0, comment='#')

    def flagdict(self, platform):
        plat = dict(affy=None, ag='.txt:gFEFlags', acm='.txt:gIsWellAboveBG_Call')
        if not plat.get(platform):
            raise KeyError(u'{0:s}是不可用的，可用的参数为ag(Agilent标准芯片),acm(Agilent)定制芯片'.format(platform))
        self.flag = {n: n + plat.get(platform) for n in self._samples}

    def datadict(self, platform):
        plat = dict(affy='', agm='', agmi='')
        if not plat.get(platform):
            raise KeyError('%s不可用，可用参数如下:affy, agm(AgilentmRNA芯片),agmi(AgilentmiRNA芯片)' % platform)
        self.norm = {sample: sample + plat.get(platform) for sample in self._samples}

    def calc(self):
        for groupname, (treats, controls) in self._group:
            pass
