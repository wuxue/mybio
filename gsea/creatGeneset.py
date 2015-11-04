import pickle
from collections import defaultdict
from glob import glob

f1 = 'anno.pkl'
f2 = glob('*.pkl')
f2 = [n for n in f2 if n != f1]

f1 = open(f1, 'rb')
anno = pickle.load(f1)

def url(name, ID):
    if 'KEGG' in name:
        ID = ID.split(':')[1]
        url = 'http://www.genome.jp/kegg-bin/show_pathway?%s' % ID
    else:
        url = 'http://amigo.geneontology.org/amigo/term/%s' % ID
    return url
    
def creatgsea(file, anno):
    f2 = open(file, 'rb')
    term = pickle.load(f2)
    temp = defaultdict(set)
    for gene, pas in term.items():
        for pa in pas:
            temp[pa].add(gene)
    res = []
    for pa, genes in temp.items():
        term = anno[pa]
        ul = url(file, pa)
        genes = [anno[n] for n in genes]
        genes = '\t'.join(genes)
        line = '%(term)s\t%(ul)s\t%(genes)s\n' % vars()
        res.append(line)
        
    with open('%s.gmt' % file[:-4], 'w') as fd:
        fd.writelines(res)
    print(file, 'OK')
    
for file in f2:
    creatgsea(file, anno)


