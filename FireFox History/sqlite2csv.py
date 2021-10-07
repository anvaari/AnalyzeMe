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
    places2csv get database path as input and extract places info from it, return it as dataframe and save it in output path as CSV.
    
    Parameters
    ----------
    db_path : str
        Path to sqlite database
    output_path : str
        Path to where you want to save CSV

    Returns
    -------
    places : DataFrame
        moz_places table from sqlite database in DataFrame fromat.
        Also save places DataFrame in output folder with csv format.

    '''
    con=sqlite3.connect(db_path) # Connect to database
    places=pd.read_sql_query('SELECT * FROM moz_places',con)
    if __name__=='__main__':
        places.to_csv(output_path+'/places.csv')
    con.close()
    return places
    
def history_v2csv(db_path,output_path=script_path):
    '''
    history_v2csv get database path as input and extract history info from it, return it as dataframe and save it in output path as CSV.


    Parameters
    ----------
    db_path : str
        Path to sqlite database
    output_path : str
        Path to where you want to save CSV

    Returns
    -------
    history_v : DataFrame
        moz_historyvisit table from sqlite database in DataFrame fromat.
        Also save history_v DataFrame in output folder with csv format.


    '''
    con=sqlite3.connect(db_path) # Connect to database
    history_v=pd.read_sql_query('SELECT * FROM moz_historyvisits', con)
    if __name__=='__main__':
        history_v.to_csv(output_path+'/history_visit.csv')
    con.close()
    return history_v

def origins2csv(db_path,output_path=script_path):
    '''
    origins2csv get database path as input and extract origins info from it, return it as dataframe and save it in output path as CSV.


    Parameters
    ----------
    db_path : str
        Path to sqlite database
    output_path : str
        Path to where you want to save CSV

    Returns
    -------
    origins : DataFrame
        moz_originss table from sqlite database in DataFrame fromat.
        Also save origins DataFrame in output folder with csv format.
    '''
    con=sqlite3.connect(db_path)  # Connect to database
    origins=pd.read_sql_query('SELECT * FROM moz_origins', con)
    if __name__=='__main__':
        origins.to_csv(output_path+'/origins.csv')
    con.close()
    return origins
    
    
    
    
if __name__=='__main__':
    # Parse arguments
    parser=argparse.ArgumentParser(description='Convert your firefox history from sqlite to csv format')
    parser.add_argument(
        '--db',
        dest='db_path',
        type=str,
        default=f'{script_path}/places.sqlite',
        help='Path to sqlite database. [Default is : path/to/code/places.sqlite]')
    parser.add_argument(
        '--output',
        dest='output_path',
        type=str,
        default=script_path,
        help='Path to where you want csv files save')
    # Assign argumnets to variables 
    args=parser.parse_args()
    db_path=args.db_path
    output_path=args.output_path
    
    if not os.path.isfile(db_path):
        raise Exception("\ndatabase path is not valud. Please provide valid address to your Firefox sqlite database")
    # Export tables in sqlite database as CSV
    places2csv(db_path,output_path)
    history_v2csv(db_path, output_path)
    origins2csv(db_path, output_path)
    
    