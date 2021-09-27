import pandas as pd 
import numpy as np
import dask.dataframe as dd
import ProperDict as PropD
import dask
import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile, io
import json
import matplotlib.pyplot as plt 
import seaborn as sns

# final class for company filings
class CompanyFilings:
    # , num: pd.DataFrame(), pre: pd.DataFrame(), dim: pd.DataFrame(), sub: pd.DataFrame(), tag: pd.DataFrame()
    def __init__(self, ticker=' ', name=' ', cik=' '):
        self.ticker, self.name, self.cik = self._get_company_name(ticker.lower(), name.lower(), cik.lower())
        self._valid_statements = ['BS','CF','IS']
        self._valid_forms = ['10-K', '10-Q']
        self._valid_timeframes = ['yearly', 'quarterly']
        self.collect_filings()
    
    # TODO
    # - add NLP functionality
    # - add 8-K functionality -- not yet supported by xbrl 

    def extract_statement(self, adsh: str, statement='BS') -> pd.DataFrame():
        form_type = self.sub[self.sub['adsh'] == adsh]['form'].iloc[0]
        date_filed = self.sub[self.sub['adsh'] == adsh]['filed'].iloc[0]
        dim  = self.collect_dim(str(date_filed))
        data_tags = self.collect_tag(adsh)
        
        cnum = self.collect_num(adsh)
        cpre = self.collect_pre(adsh, stmt=statement)

        if statement == 'IS':
            # income statement is period-dependant
            qtr = 4 # base is 4 quarters (annual report)
            if form_type == '10-Q':
                qtr = 1
            common_tags = pd.merge(cnum[cnum['qtrs'] == qtr], cpre[['tag','plabel', 'line']], on='tag')
        else:
            common_tags = pd.merge(cnum, cpre[['tag','plabel', 'line']], on='tag')
        
        promoted_dims = self._promote_dimh(cnum, cpre, dim)
        extract_promoted = self._extract_promoted(common_tags, promoted_dims, data_tags)
        return extract_promoted

    def collect_num(self, adsh: str) -> pd.DataFrame():
        numd = PropD.NUM
        numo = {key:value[len(value)-1] for (key,value) in numd.items()}

        date_filed = self.sub[self.sub['adsh'] == adsh]['filed'].iloc[0]
        period = self.sub[self.sub['adsh'] == adsh]['period'].iloc[0]
        fdir = self._get_directory(str(date_filed))
        
        qt = 4
        if self.sub[self.sub['adsh'] == adsh]['form'].iloc[0] == '10-Q':
            qt = 1
        
        num = dd.read_csv(f'F:\LPS\SEC_DB\{fdir}\\num.tsv', sep='\t', dtype=numo, error_bad_lines=False)
        cnum = num[(num.adsh == adsh) & (num.ddate == period) & (num.qtrs.isin([qt, 0]))].compute()
        cnum.drop_duplicates(subset=['tag','dimh','value'],inplace=True)
        return cnum

    def collect_pre(self, adsh: str, stmt='BS') -> pd.DataFrame():
        prep = PropD.PRE
        pred = {key:value[len(value)-1] for (key,value) in prep.items()}

        date_filed = self.sub[self.sub['adsh'] == adsh]['filed'].iloc[0]
        fdir = self._get_directory(str(date_filed))
        pre = dd.read_csv(f'F:\LPS\SEC_DB\{fdir}\\pre.tsv', sep='\t', dtype=pred, error_bad_lines=False, blocksize=None) #no other choice...
        
        cpre = pre[(pre.adsh == adsh) & (pre.stmt == stmt)].compute()
        cpre.sort_values(by='line', inplace=True)
        return cpre

    def collect_tag(self, adsh: str) -> pd.DataFrame():
        tog = PropD.TAG
        togd = {key:value[len(value)-1] for (key,value) in tog.items()}

        date_filed = self.sub[self.sub['adsh'] == adsh]['filed'].iloc[0]
        fdir = self._get_directory(str(date_filed))
        tag = pd.read_csv(f'F:\LPS\SEC_DB\{fdir}\\tag.tsv', sep='\t', dtype=togd, error_bad_lines=False)
        return tag

    def collect_dim(self, date_filed: int) -> pd.DataFrame():
        dime = PropD.DIM
        dimed = {key:value[len(value)-1] for (key,value) in dime.items()}

        fdir = self._get_directory(date_filed)
        dim = dd.read_csv(f'F:\LPS\SEC_DB\{fdir}\\dim.tsv', sep='\t', dtype=dimed, error_bad_lines=False)
        dim = dim.compute()
        return dim
    
    def collect_filings(self) -> pd.DataFrame():
        subd = PropD.SUB
        subdd = {key:value[len(value)-1] for (key,value) in subd.items()}
        
        load = dd.read_csv('F:\LPS\SEC_DB\*\sub.tsv', blocksize=16 * 1024 * 1024, sep='\t', dtype=subdd)
        subm = load[load.cik == self.cik].compute(scheduler='processes', num_workers=4)
        self.sub = subm.sort_values(by='filed', ascending=False)
        return self.sub 
    # -----------------------------------------------

    def _get_company_name(self, ticker:str, name:str, cik:str) -> float:
        os.chdir('F:\LPS')
        if not ticker or not name or not cik: 
            raise ValueError('No names/values given')
        company_entry = {}
        with open('company_tickers.json', 'r') as tick:
            ticker_set = json.load(tick)
            for entry in ticker_set.values():
                if entry['cik_str'] == cik or entry['ticker'].lower() == ticker or entry['title'].lower() == name:
                    company_entry = entry
                    break
            if len(company_entry) == 0: raise ValueError('Company does not exist')
        
        print(f"Title: {company_entry['title'].upper()} \nTicker: {company_entry['ticker'].upper()} \ncik: {company_entry['cik_str']}")
        return company_entry['ticker'], company_entry['title'].lower(), company_entry['cik_str']

    def _get_quarter(self, month:str) -> str:
        if month[0] == '0':
            month = month[1]
        month = int(month)
        if month < 4:
            return 'Q1'
        elif month < 7:
            return 'Q2'
        elif month < 10:
            return 'Q3'
        elif month <= 12:
            return 'Q4'

    def _get_directory(self, date: str) -> str:
        #20091231
        #YYYY MM DD
        if int(date[:6]) >= 202010:
            return date[:4] + '-' + date[4:6] 
        regstr =  date[:4] +'-'+ self._get_quarter(date[4:6])
        return regstr

    # filtering and extracting data from the datasets
    # selects [terms with brackets] from the dataframe, and adds them to a list
    def _dimensionals(self, pre: pd.DataFrame()) -> list: 
        dimensional = pre[pre['plabel'].str.contains(r'\[', na=False)]['plabel']
        labels = []
        for i in range(1, dimensional.shape[0]):
            current = dimensional.iloc[i]
            row_buffer = ''
            for letter in current:
                if letter == ' ':
                    continue
                elif letter == '[':
                    break
                else:
                    row_buffer += letter
            if row_buffer not in labels:
                labels.append(row_buffer)
            else:
                continue
        return labels

    # splits dimension arguments into a parseable list
    def _dim_splitter(self, dimslice: pd.DataFrame()) -> list:
        segs = dimslice.split(';')[:-1]
        key_values = [x.split('=') for x in segs]
        return key_values

    # creates ranking based on how many 'hits' each value's dimhash value had (compared to the _dimensionals found)
    def _promote_dimh(self, num: pd.DataFrame(), pre: pd.DataFrame(), dim: pd.DataFrame()) -> dict:
        hashes = dim[dim['dimhash'].isin(num['dimh'])]
        plabels = self._dimensionals(pre)

        hash_rank = {}
        hash_rank.update({'0x00000000' : -1})
        for i in range(hashes.shape[0]):
            ranking = 0
            if hashes['dimhash'].iloc[i] == '0x00000000':
                continue

            segmented = self._dim_splitter(hashes['segments'].iloc[i])
            for kv in segmented:
                for val in kv:
                    if val in plabels:
                        ranking += 1
            hash_rank.update({hashes['dimhash'].iloc[i] : ranking})
        return hash_rank

    # the actual ranking engine, selects the most relevant values based on their dimhash ranking and iprx value
    def _extract_promoted(self, common_tags: pd.DataFrame(), promoted_dims: dict, data_tags: pd.DataFrame()) -> pd.DataFrame():
        df_list = []
        uniq = list(common_tags['tag'].unique())
        
        i = 0
        for tag in uniq:
            matches = common_tags[common_tags['tag'] == tag]
            matches['rank'] = [promoted_dims[ky] for ky in matches['dimh']]
            
            rmax = matches['rank'].max()
            rmin = matches['rank'].min()
            imin = matches['iprx'].min()

            if rmax > 0:
                up_match = matches[matches['rank'] == rmax]
                if up_match.shape[0] > 1:
                    up_match = up_match[up_match['iprx'] == imin]
            else:
                up_match = matches[matches['rank'] == rmin]
                if up_match.shape[0] > 1:
                    up_match = up_match[up_match['iprx'] == imin]
            df_list.append(up_match)
            i += 1

        # econt = pd.concat(df_list)
        ep = pd.concat(df_list)
        # ep = self._verify_crdr(econt, data_tags)
        ep.insert(1, 'plabel', ep.pop('plabel'))
        ep.insert(2, 'value', ep.pop('value'))
        ep.drop(['footnote', 'dimn', 'coreg', 'durp', 'datp', 'dcml', 'footlen'], axis=1, inplace=True)
        ep.sort_values(by='line', inplace=True)
        ep.dropna(how='all', inplace=True)
        ep.fillna(0)
        return ep

class FilingsDownloader:
    def __init__(self):
        self.dlinks, self.downloads = self._collect_links()
        self.current = self._current()

    # downloads and extracts entire database from SEC website
    def download_entire_database(self, datapath: str):
        i = 0
        for link in self.downloads:
            fname = link.string.replace(" ", "-")
            os.mkdir(datapath + "\\" + fname)
            
            print(f"Now Downloading: {fname}... ")
            r = requests.get(self.dlinks[i], stream=True)
            
            zipper = zipfile.ZipFile(io.BytesIO(r.content))
            print(f"Extracting {fname}...")
            zipper.extractall(datapath + "\\" + fname)
            
            print(f"Downloaded and Extracted {fname}.\n")
            i += 1
    
    def download_update(self, datapath:str):
        i = 0
        for link in self.downloads:
            comp = link.string.replace(" ", "-")
            if comp not in self.current:
                os.mkdir(datapath + "\\" + comp)

                print(f"Now Downloading: {comp}... ")
                r = requests.get(self.dlinks[i], stream=True)
                
                zipper = zipfile.ZipFile(io.BytesIO(r.content))
                print(f"Extracting {comp}...")
                zipper.extractall(datapath + "\\" + comp)
                
                print(f"Downloaded and Extracted {comp}.\n")
            i += 1

    def download_company_name(self):
        tik = requests.get('https://www.sec.gov/files/company_tickers.json')
        os.chdir('F:\LPS')
        print(f'Downloaded at:{os.getcwd()}')
        with open('ticker_set.json', 'wb') as ticker:
            ticker.write(tik.content)

    def company_name_search(self, name=' ') -> None:
        os.chdir('F:\LPS')
        finds = []
        with open('ticker_set.json', 'r') as tick:
            ticker_set = json.load(tick)
            for entry in ticker_set.values():
                if re.search(name.lower(), entry['title'].lower()):
                    finds.append(entry)
        for x in finds: print(x)

    def _current(self):
        os.chdir('F:\LPS\SEC_DB')
        return os.listdir(os.getcwd())

    def _collect_links(self):
        # script to collect all download links
        URL = 'https://www.sec.gov/dera/data/financial-statement-and-notes-data-set.html'
        r = requests.get(URL)

        soup = BeautifulSoup(r.content, 'html5lib')

        downloads = soup.find_all(href=re.compile('financial-statement-and-notes-data-sets'))
        dlink = ["https://www.sec.gov/" + downloads[i]['href'] for i in range(len(downloads))] 
        return dlink, downloads

def VisualizeRange(ranged:pd.DataFrame(), rows:list, figsize=(10,5)):
    plt.figure(figsize=figsize)
    names = [ranged['plabel'].iloc[x] for x in rows]
    if len(names) > 7:
        title = 'Various Entries' 
    else:
        title = ' vs '.join(names)

    for r in rows:
        plt.plot([x for x in ranged.columns[3:-4]], ranged[ranged.columns[3:-4]].iloc[r], label=ranged['plabel'].iloc[r])
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def RangedFilings(filings: CompanyFilings, statement='BS', form='10-K') -> pd.DataFrame():
    filing_list = []
    subm = filings.sub[filings.sub['form'] == form]
    
    for i in range(subm.shape[0]):
        cadsh = subm['adsh'].iloc[i]
        print('Compiling: ', filings._get_directory(str(int(subm['filed'].iloc[i]))))
        filing_list.append(filings.extract_statement(cadsh, statement=statement)) # most time spent here
        
    filing_list[0].rename(columns={'value' : filing_list[0]['ddate'].iloc[0]}, inplace=True)
    cdf = filing_list[0]
    for f in range(1, len(filing_list)):
        val_date = str(filing_list[f]['ddate'].iloc[0])
        filing_list[f].rename(columns={'value' : val_date}, inplace=True)
        filing_list[f] = filing_list[f][['plabel', val_date]]
        cdf = pd.merge(cdf, filing_list[f], on=['plabel'], how='outer')
    
    cdf.drop_duplicates(subset=['plabel'], inplace=True)
    cdf.drop(['tag','ddate', 'dimh', 'iprx'],axis=1, inplace=True)
    cdf.insert(len(cdf.columns)-1, 'version', cdf.pop('version'))
    cdf.insert(len(cdf.columns)-1, 'qtrs', cdf.pop('qtrs'))
    cdf.insert(len(cdf.columns)-1, 'line', cdf.pop('line'))
    cdf.insert(len(cdf.columns)-1, 'rank', cdf.pop('rank'))
    cdf.insert(1, 'uom', cdf.pop('uom'))
    cdf.reset_index(inplace=True)
    cdf.drop(['index'], axis=1, inplace=True)
    return cdf