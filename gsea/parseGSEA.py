# -*- coding: gb2312 -*-
"""
Created on Tue Aug 18 14:58:54 2015

@author: wu
"""

from collections import defaultdict
from Bio.KEGG import REST


org = 'mmu'

res = REST.kegg_link('pathway', org)
for line in res:
    line = line.decode()
    