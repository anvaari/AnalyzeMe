"""
@author: zil.ink/anvaari
"""
import sqlite3
import pandas as pd
import argparse
import os

# Specify path where this code exist
script_path=os.path.dirname(os.path.abspath(__file__))

def places2csv(db_path,output_path=script_path):
    '''
    

    Parameters
    ----------
    db_path : str
        Path to places.sqlite.
    output_path : str
        Path where csv files will save.

    Returns
    -------
    places : DataFrame
        moz_places table from places.sqlite in DataFrame fromat.
        Also save places DataFrame in output folder with csv format.

    '''
    con=sqlite3.connect(db_path)
    places=pd.read_sql_query('SELECT * FROM moz_places',con)
    if __name__=='__main__':
        places.to_csv(output_path+'/places.csv')
    con.close()
    return places
    
def history_v2csv(db_path,output_path=script_path):
    '''
    

    Parameters
    ----------
    db_path : str
        Path to places.sqlite.
    output_path : str
        Path where csv files will save.

    Returns
    -------
    history_v : DataFrame
        moz_historyvisit table from places.sqlite in DataFrame fromat.
        Also save history_v DataFrame in output folder with csv format.


    '''
    con=sqlite3.connect(db_path)
    history_v=pd.read_sql_query('SELECT * FROM moz_historyvisits', con)
    if __name__=='__main__':
        history_v.to_csv(output_path+'/history_visit.csv')
    con.close()
    return history_v

def origins2csv(db_path,output_path=script_path):
    '''
    

    Parameters
    ----------
    db_path : str
        Path to places.sqlite.
    output_path : str
        Path where csv files will save.

    Returns
    -------
    origins : DataFrame
        moz_originss table from places.sqlite in DataFrame fromat.
        Also save origins DataFrame in output folder with csv format.
    '''
    con=sqlite3.connect(db_path)
    origins=pd.read_sql_query('SELECT * FROM moz_origins', con)
    if __name__=='__main__':
        origins.to_csv(output_path+'/origins.csv')
    con.close()
    return origins
    
    
    
    
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Convert your firefox history from sqlite to csv format')
    parser.add_argument(
        '--db-path',
        dest='db_path',
        type=str,
        help='Path to places.sqlite')
    parser.add_argument(
        '--output-path',
        dest='output_path',
        type=str,
        default=os.getcwd(),
        help='Path to where you want csv files save')
    args=parser.parse_args()
    db_path=args.db_path
    output_path=args.output_path
    p=places2csv(db_path,output_path)
    v=history_v2csv(db_path, output_path)
    o=origins2csv(db_path, output_path)
    
    