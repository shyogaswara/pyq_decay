#!/usr/bin/env python

'''
Provides method to convert BMKG EQ short messages into tabular data. 
DataReader will be used to read data and convert those data into
dataframe. _multi method will be used to read line by line from file
and then the line will be splitted into dataframe by raw2df method.


[UPDATE NOTES]
4 Nov 2021 - Version 1.0.0
- initial release

[BUG NOTES]
- Getting ValueError when reading file that have short messages from
KSI (already issued alpha release fix, will be fixed in the next patch)

'''
import io
import os
import re

import pandas as pd

from datetime import datetime


__author__ = 'Shandy Yogaswara'
__copyright__ = 'Copyright 2021, PyQ Decay Calculator'
__license__= 'GPL-3.0'
__version__ = '1.0.0'
__email__ = 'sh.yogaswara@gmail.com'
__status__ = 'Development'

class DataReader():
    
    def raw2df(self,df):
        df['M'] = df[0].str[-3:]
        df['M'] = df['M'].astype(float)
        #date & hour#
        df['Tgl'] = df[1].str.split(' ').str[1]
        df['Tgl'] = pd.to_datetime(df['Tgl']).dt.date
        df['Jam'] = df[1].str.split(' ').str[2]
        df['Jam'] = pd.DatetimeIndex(df['Jam']).time
        #lintang#
        lin = df[2].str.split(':').str[1]
        df['Lin'] = lin.str.split(' ').str[0]
        df['Lin'] = df['Lin'].astype(float)
        df['lin_1'] = lin.str.split(' ').str[1]
        df.loc[df['lin_1'] == 'LS','Lin'] = df['Lin']*-1
        #bujur#
        df['Buj'] = df[3].str.split(' BT ').str[0]
        df['Buj'] = df['Buj'].astype(float)
        df['Lok'] = df[3].str.split(' BT ').str[1]
        df['Lok'] = df['Lok'].str[1:-1]
        #kdlmn#
        dlm = df[4].str.split('Km').str[0]
        df['Kdlmn'] = dlm.str.split(':').str[1]
        df['Kdlmn'] = df['Kdlmn'].astype(float)
        #ket#
        Ket = df[4].str.split('dirasakan di ').str[1]
        try:
            df['Ket'] = Ket.str.split(' ::').str[0]
        except:
            df['Ket'] = Ket
        df['Ket'].fillna('Tidak Dirasakan', inplace=True)
        df['Origin'] = df[4].str.split('::').str[1]
        df = df[['Tgl','Jam','Lin','Buj','M','Kdlmn','Lok','Ket','Origin']]
        df = df.sort_values(by=['Tgl','Jam'])
        df = df.reset_index(drop=True)
        return df

        
    def _multi(self,filename): # read raw data and convert it to usable dataframe for database input, create map, or histogram 
        for_pd = io.StringIO()
        with open(filename) as f:
            for line in f:
                new_line = re.sub(r',', '|', line.rstrip(), count=4)
                print (new_line, file=for_pd)
        for_pd.seek(0)
        df = pd.read_csv(for_pd, sep='|',engine='python', header=None)
        for_pd.close()
        df = self.raw2df(df)
        return df

    def csv2df(self,filename,header):
        if header<0:
            header=None
        df = pd.read_csv(filename, engine='python', header=header)
        return df

    def df2csv(self,dataframe,filename):
        df = dataframe
        df.to_csv(filename, index=False)

    def df2json(self,dataframe,filename=None):
        if filename:
            save_res = dataframe.to_json(filename, orient='index')
        result = dataframe.to_json(orient='split')
        return result


if __name__ == '__main__':
    OPEN_FILENAME = ''
    SAVE_FILENAME = ''
    _reader = InfoGempaReader()
    dataframe = _reader._multi(filename=OPEN_FILENAME)
    dataframe = _reader.raw2df(df=dataframe)
    _reader.df2csv(dataframe=dataframe,filename=SAVE_FILENAME)