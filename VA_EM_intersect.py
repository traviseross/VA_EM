import pandas as pd
import itertools
import numpy as np
with open('/Users/travisross/travisross/VA_EM/VA_corpus_PMIDs.txt','r') as f:
    VA_pmids=[line.rstrip() for line in f]
    f.close()
with open('/Users/travisross/travisross/VA_EM/EM_corpus_PMIDs.txt','r') as f:
    EM_pmids=[line.rstrip() for line in f]
    f.close()
VA_EM_pmids=list(set(VA_pmids).intersection(EM_pmids))
with open('/Users/travisross/travisross/VA_EM/VA_EM_crossover_PMIDs.txt','w') as f:
    for pmid in VA_EM_pmids:
        f.write(pmid+'\n')
    f.close()
with open('/Users/travisross/travisross/VA_EM/VA_corpus.tsv','r') as f:
    df=pd.read_csv(f,sep='\t')
    f.close()
df_filtered = df[np.isin(df['pmid'].to_numpy(), VA_EM_pmids)]
df_filtered.to_csv('/Users/travisross/travisross/VA_EM/VA_EM_corpus.tsv',sep='\t',index=False)