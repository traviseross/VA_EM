from tkinter import N
import requests
import lxml
import pandas as pd
from bs4 import BeautifulSoup as bs
from time import sleep
import math
import pymed
import metapub
fetch = metapub.PubMedFetcher()
api_key='6e902c74ef429caa9b724d4796a2883c3408'#input("Enter your API key: ")
queries=[
	"%22Emergency%20Medicine%22%5BMESH%5D%20OR%20%28%28%28%28%28%28%28%22The%20American%20journal%20of%20emergency%20medicine%22%5BJournal%5D%29%20OR%20%28%22Annals%20of%20emergency%20medicine%22%5BJournal%5D%29%29%20OR%20%28%22The%20Journal%20of%20emergency%20medicine%22%5BJournal%5D%29%29%20OR%20%28%22Academic%20emergency%20medicine%20%3A%20official%20journal%20of%20the%20Society%20for%20Academic%20Emergency%20Medicine%22%5BJournal%5D%29%29%20OR%20%28%22Pediatric%20emergency%20care%22%5BJournal%5D%29%29",
	"VA+Hospital%5BAffiliation%5D+OR+VA+Medical%5BAffiliation%5D+OR+VA+Health%5BAffiliation%5D+OR+VA+Healthcare%5BAffiliation%5D+OR+VAMC%5BAffiliation%5D+OR+Veterans%5BAffiliation%5D+OR+VHA%5BAffiliation%5D+OR+%40va.gov%5BAffiliation%5D"
]

def parse_pmid(id):
	article = fetch.article_by_pmid(id)
	dict_out={}
	try:
		dict_out['title']=article.title
	except Exception as e:
		print(f'error on title: {e}')
		pass
	try:
		dict_out['year']=article.year
	except Exception as e:
		print(f'error on year: {e}')
		pass
	try:
		dict_out['auth_count']=len(article.authors)
	except Exception as e:
		print(f'error on year: {e}')
		pass
	try:
		if isinstance(article.authors, list):
			if len(article.authors)>10:
				i=0
				for author in article.authors[:10]:
					dict_out[f'auth_{i}']=author
					i+=1
				dict_out['auth_additional']=article.authors[10:]
			elif len(article.authors)<11:
				for idx,author in enumerate(article.authors):
					dict_out[f'auth_{idx}']=author
			else:
				dict_out['authors']=article.authors
		elif isinstance(article.authors, str):
			dict_out['auth_0']=article.authors
		else:
			dict_out['authors']=article.authors
	except Exception as e:
		print(f'error on authors: {e}')
		pass
	try:
		dict_out['journal']=article.journal
	except Exception as e:
		print(f'error on Journal: {e}')
		pass
	try:
		dict_out['doi']=article.doi
	except Exception as e:
		print(f'error on DOI: {e}')
		pass
	try:
		dict_out['pmid']=article.pmid
	except Exception as e:
		print(f'error on PMID: {e}')
		dict_out['pmid']=id
	return(dict_out)

def pmid_getter(query):
	ids=[]
	n=1
	url=f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&{api_key}&rettype=uilist&retmode=xml&mindate=1980&maxdate=2020&retmax=10000"
	r=requests.post(url)
	soup=bs(r.content,features="lxml")
	try:
		count=int(soup.find('count').text)
		n=math.ceil(count/10000+.5)
		print(count,n)
	except Exception as e:
		print(f'error on count: {e}, trying again')
		r=requests.post(url)
		sleep(1)
		soup=bs(r.content,features="lxml")
		try:
			count=int(soup.find('count').text)
			n=math.ceil(count/10000+.5)
			print(count,n)
		except Exception as e:
			print(f'error on count: {e}, giving up')
			n=25
	for i in range(n):
		start=i*10000
		url=f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&{api_key}&rettype=uilist&retmode=xml&mindate=1980&maxdate=2020&retmax=10000&retstart={start}"
		r=requests.post(url)
		soup=bs(r.content,features="lxml")
		ids=ids+[id.text for id in soup.find_all('id')]
		ids=list(set(ids))
	return(ids)

def pmid_searcher(queries):
	id_lists=[]
	for i in range(len(queries)):
		ids=pmid_getter(queries[i])
		with open(f'/Users/travisross/travisross/VA_EM/query_{i}.txt', 'w') as f:
			for id in ids:
				f.write(f'{id}\n')
		f.close()
		id_lists.append(ids)
	return(id_lists)

if queries==[]:
	search='go on'
	while search != 'n':
		search=input("More queries? 'n' to stop\n")
		if search == 'n':
			pass
		else:
			queries.append(search)
id_lists=pmid_searcher(queries)
for i in range(len(id_lists)):
	ids_to_check=id_lists[i]
	dict_list=[]
	print(f'doing list {i} now')
	for id in ids_to_check:
		print(f"doing {id} now")
		try:
			dict_out=parse_pmid(id)
			dict_list.append(dict_out)
		except Exception as e:
			print(f'error on {id}: {e}')
			dict_list.append({'pmid':id})
			pass
	column_names=list(set().union(*(d.keys() for d in dict_list)))
	column_names.sort()
	print(column_names)
	df=pd.DataFrame(dict_list,columns=column_names)
	print(df)
	df.to_csv(f'/Users/travisross/travisross/VA_EM/query_{i}.tsv',sep='\t')
