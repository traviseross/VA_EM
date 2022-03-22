import requests
import lxml
import pandas as pd
from bs4 import BeautifulSoup as bs
from time import sleep
start=0
api_key='6e902c74ef429caa9b724d4796a2883c3408'
queries=['''%22Emergency%20Medicine%22%5BMESH%5D%20OR%20%28%28%28%28%28%28%28%22The%20American%20journal%20of%20emergency%20medicine%22%5BJournal%5D%29%20OR%20%28%22Annals%20of%20emergency%20medicine%22%5BJournal%5D%29%29%20OR%20%28%22The%20Journal%20of%20emergency%20medicine%22%5BJournal%5D%29%29%20OR%20%28%22Academic%20emergency%20medicine%20%3A%20official%20journal%20of%20the%20Society%20for%20Academic%20Emergency%20Medicine%22%5BJournal%5D%29%29%20OR%20%28%22Pediatric%20emergency%20care%22%5BJournal%5D%29%29''','%22Veteran%22[Affiliation]']
def pmid_getter(query):
	ids=[]
	for i in range(10):
		start=i*10000
		url=f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&{api_key}&rettype=uilist&retmode=xml&mindate=1980&maxdate=2020&retmax=10000&retstart={start}"
		r=requests.post(url)
		sleep(2)
		soup=bs(r.content,features="lxml")
		ids=ids+[id.text for id in soup.find_all('id')]
		ids=list(set(ids))
	return(ids)
id_lists=[]
for i in range(len(queries)):
	id_lists=id_lists + pmid_getter(queries[i])
for i in range(len(queries)):
	with open(f'/Users/travisross/travisross/VA_EM/query_{i}.txt', 'w') as f:
		for n in range(len(queries)):
			for id in id_lists[n]:
				f.write(id)
	f.close()
