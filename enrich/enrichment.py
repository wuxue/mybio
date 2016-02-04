#-*- coding:utf-8 -*-

from glob import glob
from scipy.stats import fisher_exact
from collections import defaultdict
from statsmodels.stats import multitest as mul
from numpy import log10
import os
import pandas as pd
from mybio.enrich import HTML
from mybio.enrich import plot
import pickle
import mybio
import logging

__all__ = ['analysis']


def count(genedict):

    termdict = defaultdict(set)
    for gene, terms in genedict.items():
        for term in terms.split(';'):
            termdict[term].add(gene)
    return termdict


def geturl(name, term, gene, generegulation=None):
    color = {'up': 'red', 'down': 'green', 'other': 'yellow'}
    if name.startswith('KEGG'):
        try:
            url1 = 'http://www.kegg.jp/kegg-bin/show_pathway?%s/' % (term.split(':')[1])
        except IndexError:
            return ''
        res = []
        for g in gene:
            if generegulation:
                bgcolor = color.get(generegulation[g], 'blue')
            else:
                bgcolor = 'yellow'

            res.append(g + '%09' + bgcolor)

        url = url1 + '/'.join(res)
        return url
    else:
        url = r'http://amigo.geneontology.org/amigo/term/%s' % term
        return url


def enrichment(genes, popfile, fgname, generegulation=None, myfilter=[5, 2000],
               org='hsa', go=None, kegg=None, pvalue=0.1, anno=None, **kwargs):
    """富集分析主程序

    Parameters
    ----------
    kwargs:其他参数
    anno:基因，Term的注释信息
    pvalue:网页文件中的Pvalue阈值
    kegg:KEGG文件夹
    go:GO文件
    org:物种
    myfilter:过滤条件
    generegulation:基因上下调情况
    fgname:分组名称
    popfile:数据库
    genes:差异基因list
    """
    dbname = os.path.basename(popfile)[:-4]
    head = ('Term_ID\tTerm_description\tTerm_url\tListHit\tListTotal\tPopHit\tPopTotal'
            '\tFoldEnrichment\tGenes\tGeneSymbols\tP_value\t -log10(pvalue)').split('\t')
    #数据库中的基因
    allgenes = {n.split('\t')[0]: n.strip().split('\t')[1] for n in open(popfile)}
    #差异基因在数据库中的基因
    listgenes = {n: allgenes.get(n) for n in genes if allgenes.get(n)}
    if len(listgenes) == 0:
        logging.warn(u'差异基因在%s数据库中没有注释' % dbname)
        try:
            dbid = kwargs['iddb']
            genes = [dbid.get(n) for n in genes if dbid.get(n)]
            listgenes = {n: allgenes.get(n) for n in genes if allgenes.get(n)}
            logging.info('经过ID转换后共计%d个基因转换成功！' % len(listgenes))
        except Exception as e:
            logging.warn('ID转换不成功，error:%s' % e)
            raise ValueError
    else:
        logging.info('%d个差异基因在%s数据库中有注释。' % (len(listgenes), dbname))
    poptotal, listtotal = len(allgenes), len(listgenes)
    popterms, listterms = count(allgenes), count(listgenes)
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
        oddsratio, p_value = fisher_exact(table, 'greater')
        gene = listterms[term]
        genesy = [anno.get(n, n) for n in gene]
        url = geturl(dbname, term, gene, generegulation)
        vv = -log10(p_value)
        line = (term, anno[term], url, listhit, listtotal, pophit, poptotal,
                oddsratio, ';'.join(gene), ';'.join(genesy), p_value, str(vv))
        data.append(line)
    if len(data) == 0:
        logging.debug('Pvalue计算过程没有出结果！')
        raise ValueError('Pvalue计算不出结果')

    df = pd.DataFrame(data, columns=head)
    df = df.sort_values(by='P_value')
    fdr = df['P_value']
    reject, pvals_corrected = mul.fdrcorrection(fdr)
    df['FDR_bh'] = pvals_corrected
    tar = kegg if "KEGG" in dbname else go
    df.to_csv(r'%s\%s\%s_%s.csv' % (tar, fgname, fgname, dbname), index=False)
    plot.plmyfig(df, dbname, fgname, tar, count=20)
    df = df[df['P_value'] <= pvalue]
    HTML.df2html(df, fgname, dbname, tar)


def analysis(genes, fg, generegulation=None, myfilter=5, org='hsa', bgfiles=None,
             creatdir=True, log='analysis'):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                        filename='%s.log' % log, filemode='w+')
    if not bgfiles:
        pkgpath = mybio.__path__[0]
        bgfiles = glob(os.path.join(pkgpath, 'data', org, '*.txt'))
        anno = pickle.load(open(os.path.join(pkgpath, 'data', org, 'anno.pkl'), 'rb'))
        try:
            idconventdb = {n.split('\t')[0]:n.strip().split('\t')[1]
                           for n in open(os.path.join(pkgpath, 'data', org, 'iddb'))}
        except FileNotFoundError:
            idconventdb = {}
    else:
        bgfiles = glob(r'%s\*.txt' % bgfiles)
        anno = glob(r'%s\anno' % bgfiles)[0]
        assert anno, logging.info("注释文件不存在")
        anno = {n.split('\t')[0]: n.split('\t'[1].strip()) for n in open(anno)}
    n1 = len(genes)
    genes = set([n.strip() for n in genes])
    logging.info(fg+'starting...用于富集分析的基因共计%d个,删除重复后剩余%d' % (n1, len(genes)))
    if creatdir:
        go, kegg = 'GO Enrichment', 'KEGG Enrichment'
        try:
            os.mkdir(go)
            os.mkdir(kegg)
        except FileExistsError as e:
            logging.debug(e)
    try:
        os.mkdir(os.path.join(go, fg.strip()))
        os.mkdir(os.path.join(kegg, fg.strip()))
    except FileExistsError as e:
        logging.debug(e)
    for popfile in bgfiles:
        try:
            enrichment(genes, popfile, fg, generegulation=generegulation,
                       myfilter=myfilter, org=org, go=go, kegg=kegg,
                       anno=anno, iddb=idconventdb)
        except (AssertionError,ValueError) as e:
            logging.warn('%s without %s annotation! erroe:%s' % (fg, os.path.basename(popfile), e))
    logging.info(fg+'End..')


if __name__ == "__main__":
    print('test')
