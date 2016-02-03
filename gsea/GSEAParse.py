
import shutil
import os
import re

pa1 = re.compile(r'.+report_for_(.+?)_\d')

import mybio

def mkdir(name):
    try:
        if '\\' in name:
            os.makedirs(name)
        else:
            os.mkdir(name)
    except FileExistsError:
        pass

def mvandrename(files, root):
    mkdir(root)
    reports = [n for n in files if 'gsea_report_for' in n]
    for file in reports:
        name = pa1.findall(file)[0]
        group = r'%s\%s' % (root, name)
        shutil.copyfile(file, r'%s\%s.xls' % (root, name))
        mkdir(group)
        for i, line in enumerate(open(file)):
            line = line.split('\t')
            try:
                termname, isdata = line[0].strip(), line[2]
            except IndexError:
                continue
            if isdata.startswith('Detail'):
                term = r'%s\%d_%s' % (group, i, termname.title())
                mkdir(term)
                pa2 = re.compile(r".+[\\|enplot_]?{0:s}(_\d+)*(.png|.xls)".format(termname))
                targets = [n for n in files if pa2.match(n)]
                for target in targets:
                    tt = os.path.split(target)[1]
                    try:
                        shutil.copyfile(target, r'%s\%s' % (term, tt))
                    except FileNotFoundError:
                        print(r'%s\%s' % (term, tt))
            
        



for gsea in mybio.glob('*.Gsea.*'):
    files = mybio.glob(r'%s\*' % gsea)
    name = gsea.split('.')
    mvandrename(files, name[0])
