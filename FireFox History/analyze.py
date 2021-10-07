"""
@author: zil.ink/anvaari
"""
# import required packages

import pandas as pd # Pandas for work with tabular data

import requests # requests to send request to servers

import sqlite2csv # convert tables in sqlite database to DataFrame

import matplotlib.pyplot as plt # Plot 

from PIL import Image # Work with image files

import argparse # argparse provide capability for give input as an argument from terminal.

import favicon # Download favicons of sites

import os # os for working with files and psths

import progressbar # Show progress of analyze

from serpextract import extract # Extract search phrases from google search url

from bs4 import BeautifulSoup # bs4 for extract information from HTML

# clean_text to refine persian text
from clean_text import text_cleaner as clean
from clean_text import space_codepoints

import re # Regex

# Proccess persian text
from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems

# Import Data
def sqlite2df(db_path):
    '''
    Extract sqlite database tables and convert thme to DataFrame so we can anazlyze them.

    Parameters
    ----------
    db_path : str
        Path to sqlite database

    Returns
    -------
    places : DataFrame
        moz_places table from sqlite database in DataFrame fromat.
    history_v : DataFrame
        moz_historyvisit table from sqlite database in DataFrame fromat.
    origins : DataFrame
        moz_originss table from sqlite database in DataFrame fromat.

    '''
    places=sqlite2csv.places2csv(db_path)
    places['host']=places['rev_host'].apply(lambda x:x[-2::-1])
    history_v=sqlite2csv.history_v2csv(db_path)
    origins=sqlite2csv.origins2csv(db_path)
    return places,history_v,origins
    


def get_favicon(df):
    '''
    Get dataframe contain 'host' column, and save favicons of URLs in project_path.
    df['host'] must in this format : https://url

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame contain 'host' column. 'host' column contain Sites URL. URLs must start with https://.
    
    Returns
    -------
    df : pandas.DataFrame
        df dataframe which 'icon path' column added. each icon path in each row contain path to favicon of site in that row.

    '''
    # Check if favicons folder doesn't exist, make it.
    if not os.path.exists(os.path.join(project_path,'favicons')):
        os.mkdir(os.path.join(project_path,'favicons'))
        downloaded_fvs=[]
    else:
        downloaded_fvs=os.listdir(os.path.join(project_path,'favicons'))
        
    df['icon path']='' # Initiate icon path column
    
    # Start Download and save favicons
    print('Donwload and save Favicons:\n')
    with progressbar.ProgressBar(max_value=len(df),redirect_stdout=True) as bar:
        for index,row in df.iterrows():
            url=row['host']
            save_name=row["host"].replace("https://","").replace("http://","")
            
            check_fav=list(map(lambda x:save_name == x[:x.rfind('.')],downloaded_fvs))
            if any(check_fav):
                fave_name=downloaded_fvs[check_fav.index(True)]
                df.at[index,'icon path']=os.path.join(project_path,'favicons',fave_name)
                bar.update(index)
                continue
            
            
            try:
                icons=favicon.get(url)
            except Exception as e:
                print(f'For {row["host"]} Exception happened:\n{e}')
                df.at[index,'icon path']=''
                bar.update(index)
                continue
            
            icon=icons[0]
            if f'{icon.format}'=='svg' :
                print('svg format not supported\n')
                df.at[index,'icon path']=''
                bar.update(index)
                continue
            # Download and save founded favicon
            respond=requests.get(icon.url,stream=True)
            save_path=os.path.join(project_path,'favicons',f'{save_name}.{icon.format}')
            with open (save_path,'wb') as image:
                for chunk in respond.iter_content(1024):
                    image.write(chunk)
                    
            df.at[index,'icon path']=save_path # Save path to icon in dataframe
            bar.update(index)
    return df

    

def show_most_frecency(origins,output_path):
    '''
    Calculate and plot sites with highest frecency then save it to output path.

    Parameters
    ----------
    origins : pandas.DataFrame
        origin dataframe extracted from places.qlite.
    output_path : str
        Path to where you want plot save.
    
    Returns
    -------
    None.
    Save image in project_path

    '''
    print("\nPloting sites with most frecency\n")
    top_frec=origins.sort_values(by='frecency',ascending=False).iloc[0:10,:].reset_index(drop=True)
    top_frec['host']='https://'+top_frec['host']
    
    top_frec=get_favicon(top_frec)
    
    fig,ax=plt.subplots(1,1,figsize=(20,10))
    
    plt.title('Sites with highest frecency in your history')
    bars=ax.bar(top_frec['host'],top_frec['frecency'])
    
    # bars_height
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    heights = [bar.get_window_extent(r).height for bar in bars]
    
    for i in top_frec.index:
        im_path=top_frec.at[i,'icon path']
        if not im_path:
            print(f'Favicon for {top_frec.at[i,"host"]} not found')
            continue
        image=Image.open(im_path)
        image=image.resize((64,64))
        fig.figimage(image,xo=95+i*103,yo=heights[i]) # This number found by trial and error.
    fig.savefig(os.path.join(output_path,'Sites with highest frecency.png'),bbox_inches='tight')

def show_most_visit(places,output_path):
    '''
    Calculate and plot sites which visited most then save it to output path.

    Parameters
    ----------
    places : pandas.DataFrame
        places dataframe extracted from places.qlite.
    output_path : str
        Path to where you want plot save.

    Returns
    -------
    None.
    Save image in project_path

    '''
    print("\nPloting most visited sites\n")
    # extract sites with most visit from places dataframe
    unique_hosts=places['host'].value_counts().to_frame()
    unique_hosts['visit count']=unique_hosts['host']
    unique_hosts['host']=unique_hosts.index
    # Sort them by visit count and keep first 10
    unique_hosts=unique_hosts.sort_values(by='visit count',ascending=False).reset_index(drop=True).loc[0:9,:]
    # Add https to first of urls, get_favicon needs it
    unique_hosts['host']='https://'+unique_hosts['host']
    # Get favicon of sites
    unique_hosts=get_favicon(unique_hosts) 
    
    # Plot sites with most visit
    fig,ax=plt.subplots(1,1,figsize=(30,10))
        
    plt.title('Sites you visit most')
    bars=ax.bar(unique_hosts['host'],unique_hosts['visit count'])
    
    #  find bars height
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    heights = [bar.get_window_extent(r).height for bar in bars]
    
    # Place favicons on top of bars
    for i in unique_hosts.index:
        im_path=unique_hosts.at[i,'icon path']
        if not im_path:
            print(f'Favicon for {unique_hosts.at[i,"host"]} not found')
            continue
        image=Image.open(im_path)
        image=image.resize((64,64))
        fig.figimage(image,xo=150+i*155,yo=heights[i]) # These number calculated by trial and error
    fig.savefig(os.path.join(output_path,'Sites you visit most.png'),bbox_inches='tight') # Save image
    
    
def get_words_freq(words_list):
    '''
    This function get list of words and return dict. Keys are words and values are frequency of words in list.
    At first words normalized then stem of words userd. Then signs, words contain numbers and words which have less than 2 letter waw removed.

    Parameters
    ----------
    words_list : list
        list of words.

    Returns
    -------
    words_freq_dict : dict
        Keys are words and values are frequency of words in list.

    '''
    
    # Create a list from all text
    sentences=words_list
    
    
    # Specify Signs and Numbers in order to avoid words contain them enter in our final Set 
    signs=['،','«','»','.',')','(','"',':',';','%','-','?',',','؛',"'",'_']
    numbers=[f'{i}' for i in range(10)]
    
    # Stop words
    with open(f'{project_path}/stopwords.dat') as fp:
        stop_words=fp.readlines()
    stop_words=list(map(lambda x:x.strip(),stop_words))
    stop_words.append('های')
    
            
    # Create Set of all words in corpus
    normal=Normalizer()
    token=Tokenizer()
    stemm=FindStems()
    words_freq_dict=dict()
    
    for sentence in sentences:
        sentence=normal.normalize(sentence) # Normalize
        sentence=sentence.replace(u'\u200c',' ')
        words=token.tokenize_words(sentence) # Tokenize senteces
        for word in words:
            word=stemm.convert_to_stem(word) # Use stem of words
            
            if word in signs : # Ignore signs
                continue
            for let in word: # Ignore words contain numbers
                if let in numbers:
                    continue
            if len(word) <=1: # ignore one (or less)letter strings
                continue
            if word in stop_words: # ignore stopwords
                continue
            if word in words_freq_dict:
                words_freq_dict[word]+=1
            else:
                words_freq_dict[word]=1
            
    return words_freq_dict


def get_search_phrases(places,history_v,output_path,scrap_suggested=False):
    '''
    Extract search phrases in google.com from sqlite database. Also detect language of search phrase is whether english or persian or mixed.

    Parameters
    ----------
    places : pandas.DataFrame
        moz_places table from sqlite database in DataFrame fromat.
    history_v : pandas.DataFrame
        moz_historyvisit table from sqlite database in DataFrame fromat.
    output_path : str
        Path to where you want final CSV save.
    scrap_suggested : bool, optional
        True if you want use suggested phrase from google.com. For example if you searcg androoid, google suggest android. The default is False.

    Returns
    -------
    search_df : pandas.DataFrame
        Dateframe contain url searh, search phrase, phrase language, visit count and visit date. Also save dataframe as Google_Search_Data.csv in output_path.

    '''
    search_df=pd.DataFrame(columns=['url','search_phrase','phrase_language','visit_count','visit_date'])
    if scrap_suggested :
        search_df['suggested_phrase']=''
    eng_alph='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    h={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    print('\nStart extract searches from database')
    with progressbar.ProgressBar(max_value=len(places),redirect_stdout=True) as bar:
        for index,row in places.iterrows():
            url=row['url']
            if 'sorry' in url:
                bar.update(index)
                continue
            if 'google' not in row['host']:
                bar.update(index)
                continue
            if 'https://www.google.com/search' in url:
                search_df.at[index,'url']=url
                phrase=extract(url).keyword
                search_df.at[index,'search_phrase']=phrase
                # Check what google suggest [if scrap_suggested is on]
                if scrap_suggested :
                    try:    
                        # Find google suggestion for search phrase 
                        r=requests.get(url,headers=h)
                        bs=BeautifulSoup(r.content,'html.parser')
                        c_phrase_url=bs.find(id='taw').find('a')['href']
                        c_phrase_url='https://www.google.com'+c_phrase_url
                        c_phrase= extract(c_phrase_url).keyword
                        search_df.at[index,'suggested_phrase']=c_phrase
                    except:
                        pass
                # Replace all kinds of sapce with normal space
                phrase_alph = re.sub(r"[" +
                                space_codepoints+ "]", "", phrase)
                # Replace nim fasele with space
                phrase_alph = re.sub(r"[\u200c]", "", phrase_alph)
                # remove signs and ) and ) and ... all non alphabetic sign we may use in search
                phrase_alph = re.sub(r'''(?:\(|\)|\+|_|-|\.|,|،|\/|\\|\?|\!|%|\*|\=|'|")''',"",phrase_alph)
                # Detect if search phrase is number 
                if phrase_alph.isnumeric():
                    search_df.at[index,'phrase_language']='Number'
                else: # If it is not number, remove numbers
                    phrase_alph=re.sub(r"[0-9]","",phrase_alph)
                    # Check if phrase is english of persain or mixed 
                    eng_count=sum(list(map(lambda x: x in eng_alph,phrase_alph)))
                    if eng_count==len(phrase_alph):
                        search_df.at[index,'phrase_language']='English'
                    elif eng_count==0:
                        search_df.at[index,'phrase_language']='Persian'
                    else:
                        search_df.at[index,'phrase_language']='Mixed'
                
                search_df.at[index,'visit_count']=row['visit_count']
                
                # Add visit_date from history_v dataframe
                dates=history_v[history_v['place_id']==row['id']]['visit_date'].to_list()
                search_df.at[index,'visit_date']=','.join(list(map(lambda x:str(x),dates)))
            bar.update(index)
        
    # Refine and clean all persian phrases
    search_df.loc[search_df['phrase_language']=='Persian','search_phrase']=search_df.loc[search_df['phrase_language']=='Persian','search_phrase'].apply(lambda x: clean(x))        
    if scrap_suggested : # We may have nan value if scrap_suggested used
        search_df.loc[search_df['phrase_language']=='Persian','suggested_phrase']=search_df.loc[search_df['phrase_language']=='Persian','suggested_phrase'].apply(lambda x: clean(x) if not pd.isna(x) else '')        
        search_df.loc[:,'suggested_phrase']=search_df.loc[:,'suggested_phrase'].apply(lambda x: '' if pd.isna(x) else x)
            
    search_df.reset_index(drop=True,inplace=True) # Reset indices
    search_df.to_csv(os.path.join(output_path,'Google_Search_Data.csv')) # Save final dataframe
    return search_df

# Specify path where this code exist
project_path=os.path.dirname(os.path.abspath(__file__))

if not os.path.isfile(os.path.join(project_path,'stopwords.dat')):
    raise Exception('Please download stopwords.dat from https://github.com/sobhe/hazm/blob/master/hazm/data/stopwords.dat  and copy it in project path.')

if __name__ =='__main__':
    # Parse arguments
    parser=argparse.ArgumentParser(description='Analyze your firefox histor :)')
    parser.add_argument(
        '--db',
        dest='db_path',
        type=str,
        default=f'{project_path}/places.sqlite',
        help='Path to sqlite database. [Default is : path/to/code/places.sqlite]')
    parser.add_argument(
        '--output',
        dest='output_path',
        type=str,
        default=project_path,
        help='Path to where you want output files save. [Default is : path/to/code]')
    # Assign argumnets to variables 
    args=parser.parse_args()
    db_path=args.db_path
    output_path=args.output_path
    
    if not os.path.isfile(db_path):
        raise Exception("\ndatabase path is not valud. Please provide valid address to your Firefox sqlite database")
        
    places,history_v,origins=sqlite2df(db_path)
    show_most_frecency(origins,output_path)    
    show_most_visit(places,output_path)
    get_search_phrases(places,history_v, output_path)