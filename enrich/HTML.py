#-*- coding:gb2312 -*-


def df2html(df, fgname, bgname, tar):
    db = 'KEGG' if bgname.startswith('KEGG') else 'GO'

    head = '''
    <html>
    <head>
    <meta http-equiv='Content-Type' content='text/html; charset=gb2312'>
    <title>{0} Genes {1} Annotations</title>
    </head>                			
    <body link='#0000FF' vlink='#0000FF' alink='#0000FF'>			
    <table id='table0' style='width: 700px; border-collapse: collapse' cellPadding='0' border='0'>
    <tr>
    <td style='font-weight: 700; font-size: 10pt; vertical-align: middle; color: navy; font-style: normal; font-family: Arial, sans-serif; white-space: nowrap; height: 38pt; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <span lang='en-us' style='LETTER-SPACING: 2pt'><font size='3'>{0} Genes {1} Annotations</font></span></td>
    </tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    &nbsp;</td></tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <font face='Times New Roman' size='3'>
    <b><span lang='zh-cn'>Used notations:</span></b></font></td>
    </tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    &nbsp;</td>
    </tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul><li><font face='Times New Roman' size='3'><span lang='en-us'>
    
    <b>Term desctiption</b> - Gene category, the specific category of genes within {1}.
    
    </span> </font> </li></ul></td></tr><tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul><li><font face='Times New Roman' size='3'><span lang='en-us'>
    
    <b>List Hits</b> - The number of genes that both belong to the term and "{0}".
    
    </span> </font> </li></ul></td></tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul><li><font face='Times New Roman' size='3'><span lang='en-us'>
    
    <b>List Total</b> - The number of genes that belong to "{0}" and having at least one {1} annotation.
    
    </span> </font> </li></ul></td></tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul><li><font face='Times New Roman' size='3'>
    
    <b>Population Hits</b> - The number of genes available on the entire microarray that belong to the term(Default : Filter term which population hits less than 5).
    
    </font></li></ul></td></tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul><li><font face='Times New Roman' size='3'>
    
    <b>Population Total</b> - The number of genes available on the entire microarray and having at least one {1} annotation.
    
    </font></li></ul></td></tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul>
    <li><font face='Times New Roman' size='3'><span lang='en-us'>
    
    <b>FoldEnrichment</b> - The enrichment fold change, FoldEnrichment = (list hits/List total)/(population hits/poplation total).
    
    </span></font></li></ul></td></tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul><li><font face='Times New Roman' size='3'><span lang='en-us'>
    
    <b>P-value</b> - The probability of obtaining the term from a list of random genes.
    Less the p-value more significant is the term. The p-value is calculated with a unilateral Fisher exact test</span>.
    
    </font></li></ul></td></tr>
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul>
    <li><font face='Times New Roman' size='3'><span lang='en-us'>
    
    <b>FDR_bh</b> - Since multiple term are tested for their signficance, hence a multiple testing correction is performed.
    P-Value is corrected by FDR Benjamini-Hochberg method.
    
    </span></font></li></ul></td></tr>
    
    <tr>
    <td style='font-weight: 400; font-size: 10pt; vertical-align: middle; width: 645pt; color: windowtext; font-style: normal; font-family: Arial; white-space: nowrap; text-decoration: none; text-align: general; border: medium none; padding-left: 1px; padding-right: 1px; padding-top: 1px' align='justify'>
    <ul>
    <li><font face='Times New Roman' size='3'><span lang='en-us'>
    
    <b>NOTE:</b>This HTML file only inculde the term which P_value less than 0.1.The full result is in the CSV file.
    
    </span></font></li></ul></td></tr>
    </table>
    <br>
    '''.format(fgname, bgname)

    tail = '''
    <p>..........................................................................................................................</p>
    <td style='font-weight: 400; font-size: 10pt;vertical-align: middle;' height='340'><small>
    <small><span style="font-weight: bold;"><br>
    What's Fisher Exact and enrichment?</span> <br>
     <br>
    When members of two independent groups can fall into one of two mutually exclusive categories,
    Fisher Exact test is used to determine whether the proportions of those falling into each category differs by group.
    In OE annotation system, Fisher Exact is adopted to measure the gene-enrichment in annotation terms.<br>
      <small><span style="font-weight: bold;"><br>
      A Hypothetical Example:</span> <br>
      <br>
      </small>In human genome background (30,000 gene total), 40 genes
    are involved in p53 signaling pathway. A given gene list has found
    that 3 out of 300 belong to p53 signaling pathway. Then&nbsp; we ask
    the question if 3/300 is more than random chance comparing to the
    human background of 40/30000.<br>
      <br>
    A 2x2 contingency table is built on above numbers:<br>
          </small>
          <table style="text-align: left; height: 82px; width: 303px;"
    border="1" cellpadding="2" cellspacing="2">
        <tbody>
          <tr>
            <td style="vertical-align: top;"><small><br>
            </small></td>
            <td style="vertical-align: top;"><small>User Genes<br>
            </small></td>
            <td style="vertical-align: top;"><small>Genome<br>
            </small></td>
          </tr>
          <tr>
            <td style="vertical-align: top;"><small>In Pathway<br>
            </small></td>
            <td style="vertical-align: top; text-align: center;"><small>3
            </small></td>
            <td style="vertical-align: top; text-align: center;"><small>40<br>
            </small></td>
          </tr>
          <tr>
            <td style="vertical-align: top;"><small>Not In Pathway<br>
            </small></td>
            <td style="vertical-align: top; text-align: center;"><small>297<br>
            </small></td>
            <td style="vertical-align: top; text-align: center;"><small>29960<br>
            </small></td>
          </tr>
        </tbody>
      </table>
      <small><br>
      Fisher Exact P-Value =&nbsp; 0.008 (using 3 instead of 3-1). Since P-Value &lt;= 0.01, this
      user gene list is specifically associated (enriched) in p53 signaling
      pathway than random chance.<br></small></td>
    <p>..........................................................................................................................</p>
    This file was produced by <a target='_blank' href='http://www.oebiotech.com' style='text-decoration: none'>
    <font size='3'>OE Biotech AnalysisTeam </font></a> based on %s annotations updated on 2015.
    </body>
    </html>''' % db

    table = '''<p><b>Terms</b>(Sorted by pvalue)</p>
    <table border='1' id='table2' style='border-collapse: collapse' bordercolor='#808080'>
    <tr>
    <td align='center' width='45'><b>Rank</b></td>
    <td align='center' width='70'><b>TermID</b></td>
    <td align='center' width='200'><b>TermDescription</b></td>
    <td align='center' width='45'>
    <p style='margin-top: 0; margin-bottom: 0'><b>List </b></p>
    <p style='margin-top: 0; margin-bottom: 0'><b>Hits</b></td>
    <td align='center' width='45'>
    <p style='margin-top: 0; margin-bottom: 0'><b>List </b></p>
    <p style='margin-top: 0; margin-bottom: 0'><b>Total</b></td>
    <td align='center' width='70'>
    <p style='margin-top: 0; margin-bottom: 0'><b>Population </b></p>
    <p style='margin-top: 0; margin-bottom: 0'><b>Hits</b></td>
    <td align='center' width='70'>
    <p style='margin-top: 0; margin-bottom: 0'><b>Population </b></p>
    <p style='margin-top: 0; margin-bottom: 0'><b>Total</b></td>
    <td align='center' width='100'><b>FoldEnrichment</b></td>
    <td align='center' width='100'><b>P-value</b></td>
    <td align='center' width='100'><b>FDR_bh</b></td>
    </tr>'''

    for i, (index, row) in enumerate(df.iterrows()):
        table += '''
        <tr>
        <td align='center' width='45'><font size='3'>%i</font></td>
        <td align='center' width='70'>%s</td>
        <td align='center' width='200'><a target='_blank' href='%s' style='text-text-decoration:none'><font size='3'>%s</font></a></td>
        <td align='center' width='45'><font size='3'>%i</font></td>
        <td align='center' width='45'><font size='3'>%i</font></td>
        <td align='center' width='70'><font size='3'>%i</font></td>
        <td align='center' width='70'><font size='3'>%i</font></td>
        <td align='center' width='70'><font size='3'>%.2f</font></td>
        <td align='center' width='70'><font size='3'>%.2G</font></td>
        <td align='center' width='70'><font size='3'>%.2G</font></td>
        </tr>''' % (i, row.Term_ID, row.Term_url, row.Term_description,
                    row.ListHit, row.ListTotal, row.PopHit, row.PopTotal,
                    row.FoldEnrichment, row.P_value, row.FDR_bh)

    table += '</table>'
    with open(r'%s\%s\%s-%s.html' %
              (tar, fgname, fgname, bgname), 'w') as data:
        data.write(head + table + tail)
    print(fgname, bgname, 'HTML OK')
