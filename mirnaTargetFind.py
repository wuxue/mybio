#-*- coding:gbk -*-
'''
这个脚本用于处理miRNA靶基因关系对，
仅仅用于处理 人、小鼠、大鼠的靶基因预测关系
'''

from os import path
import mybio


def getDataPath(org):
    filePath = path.realpath(mybio.__file__)    
    dataDir = path.join(path.split(filePath)[0], 'data', 'miRNATargets', org)
    return dataDir
    
def query(mirs):
    