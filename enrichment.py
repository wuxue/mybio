#-*- coding:utf-8 -*-
__all__ = ['analysis',]
from glob import glob
from scipy.stats import fisher_exact
from collections import defaultdict
from statsmodels.stats import multitest as mul
from numpy import log10
import os
import pandas as pd
from . import HTML
from . import plot
import pickle
#description


class MyError(Exception):
    pass

def count(genedict):
    termdict = defaultdict(list)
    for gene, terms in genedict.items():
        for term in terms.split(';'):
            termdict[term].append(gene)
    return termdict

def geturl(name, term, gene, generegulation = None):
    
    color = {'up':'red', 'down':'green', 'other':'yellow'}
    if name == 'KEGG':
        url1 = 'http://www.kegg.jp/kegg-bin/show_pathway?%s/'%(term.split(':')[1])
        res  = []
        for g in gene:
            if generegulation:
                bgcolor = color.get(generegulation[g], 'blue')
            else:
                bgcolor = 'yellow'

            res.append(g + '%09' + bgcolor)

        url = url1 + '/'.join(res)
        return url
    else:
        url = r'http://amigo.geneontology.org/amigo/term/%s'%term
        return url
        
def enrichment(genes, popfile, fgname, generegulation = None, myfilter = 5, 
               org = 'hsa', go = None, kegg = None, P = 0.1, anno = None):
    
    bgname = os.path.basename(popfile)[:-4]
    head = 'Term_ID\tTerm_description\tTerm_url\tListHit\tListTotal\tPopHit\tPopTotal\tFoldEnrichment\tGenes\tGeneSymbols\tP_value\t"-log10(pvalue)"'.split('\t')
    allgenes = {n.split('\t')[0]:n.strip().split('\t')[1] for n in open(popfile)}
    listgenes = {n.strip():allgenes.get(n.strip()) for n in genes if allgenes.get(n.strip())}
    poptotal, listtotal = len(allgenes), len(listgenes)
    popterms, listterms = count(allgenes), count(listgenes)
#    df = pd.DataFrame(columns = head)
    data = []
    for term in listterms:
        listhit, pophit = len(listterms[term]), len(popterms[term])
        if isinstance(myfilter, list):
            if pophit < min(myfilter) or pophit > max(myfilter):
                continue
        else:
            if pophit < myfilter:
                continue
        table = ([listhit, listtotal - listhit], [pophit, poptotal - pophit])
        gene = listterms[term]
        genesy = [anno.get(n, '???') for n in gene]
        oddsratio, p_value = fisher_exact(table, 'greater')
        url = geturl(bgname, term, gene, generegulation)
        vv = -log10(p_value)
        line = (term, anno[term], url, listhit, listtotal, pophit, poptotal,
                oddsratio, ';'.join(gene), ';'.join(genesy), p_value, str(vv))
        data.append(line)      
    if len(data) == 0:
        raise MyError
    df = pd.DataFrame(data, columns = head)
    df = df.sort('P_value')
#    fdr = df[df['P_value'] <= 0.05]['P_value']
    fdr = df['P_value']
    reject, pvals_corrected = mul.fdrcorrection(fdr)
    df['FDR_bh'] = pvals_corrected
#    enrich.sort(key=lambda x:float(x.strip().split('\t')[-1]),reverse=False)
    if df.empty is True:
        raise MyError
    tar = kegg if "KEGG" in bgname else go
    df.to_csv(r'%s\%s\%s_%s.csv'%(tar, fgname, fgname, bgname), index = False)
    plot.plmyfig(df, bgname, fgname, tar, count = 20)
    df = df[df['P_value'] <= P]
    HTML.df2html(df, fgname, bgname, tar)


def verify(gene):
    gene = gene.strip()
    if gene.isdigit():
        return True
    else:
        return False

def analysis(genes, fg, generegulation = None, myfilter = 5, org = 'hsa', bgfiles = None,
             creatdir = True):
    
    if not bgfiles:
        bgfiles = glob(r'E:\Scripts\mypackages\mybio\data\%s\*.txt'%org)
        anno = pickle.load(open(r'E:\Scripts\mypackages\mybio\data\%s\anno.pkl'%org, 'rb'))
    else:
        bgfiles = glob(r'%s\*.txt'%bgfiles)
        anno = glob(r'%s\anno'%bgfiles)[0]
        anno = {n.split('\t')[0]:n.split('\t'[1].strip()) for n in open(anno)}

    print(fg,'starting...')
    if creatdir:
        go, kegg = 'GO Enrichment', 'KEGG Enrichment'
        try:
            os.mkdir(go)
            os.mkdir(kegg)
        except FileExistsError:
            pass
    try:
        os.mkdir(os.path.join(go,fg.strip()))
        os.mkdir(os.path.join(kegg, fg.strip()))        
    except:
        pass
    n1 = len(genes)
    genes = set([n for n in genes if verify(n)])
    print('Input ID %d, which has %s genes for analysis' % (n1, len(genes)))
    for popfile in bgfiles:
        try:
            enrichment(genes, popfile, fg, generegulation = generegulation,
                       myfilter = myfilter, org = org, go = go, kegg = kegg,
                       anno = anno)
        except MyError:
            print('%s without %s annotation!'%(fg,os.path.basename(popfile)))
    print(fg,'End..')


if __name__ == "__main__":
    print('test')
    
