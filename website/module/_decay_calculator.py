#!/usr/bin/env python

''' Provides method to calculate earthquake aftershock decay called 
DecayCalculator. This method use equation from Omori, Mogi, and Utsu
using Least Square Method. When the module called, it will read input
from either file name or dataframe that consist origin time data of
earthquake aftershock. 
The data then will be grouped by convert_time and freq_df method based
on frequency value. After that, the calc_omori, calc_mogi1, calc_mogi2,
and calc_utsu method will be used to calculate a, b, and time value 
from each equation. and then calc_nt method will be used to determine
what time when the nt equal to 1.

[UPDATE NOTES]
4 Nov 2021 - Version 1.0.0
- initial release (github.com/shyogaswara/pyq_decay)

26 Feb 2022 - Version 1.1.0
# Feature
- add calculation of n(t) that equal to 1
- add decay graphic

27 Mei 2022 - Version 1.2.0
# Feature
- add user interface with html
- added test module called _dummy.py
# Fix
- now can read data from existing dataframe instead of only csv file
refer to __init__ file for more explanation.

'''

import io
import math

import numpy as np
import pandas as pd

from datetime import timedelta

__author__ = 'Shandy Yogaswara'
__copyright__ = 'Copyright 2021, PyQ Decay Calculator'
__license__= 'GPL-3.0'
__version__ = '1.2.0'
__email__ = 'sh.yogaswara@gmail.com'
__status__ = 'Development'

class DecayCalculator:
    def __init__(self,file_name=None,dataframe=None):
        if file_name:
            self.df = pd.read_csv(file_name,engine='python',header=None)
            self.df.columns = ['count']
            
        elif not file_name:
            self.df=dataframe
        else:
            raise Exception('no input')
        self.limit = 1
        print(self.df, self.df.dtypes)

    def convert_time(self):
        try:
            self.df['count'] = (
                self.df['Tgl'].astype(str)
                +' '
                +self.df['Jam'].astype(str)
                )
        finally:
            self.df['OT'] = pd.to_datetime(self.df['count'])
            self.df.set_index('OT',inplace=True)
        return self.df[['count']].copy()

    def round_up(self,n,decimals):
        multiplier = 10**decimals
        return math.ceil(n * multiplier) / multiplier

    def round_down(self,n,decimals):
        multiplier = 10**decimals
        return math.floor(n * multiplier) / multiplier


    def freq_df(self,dataframe,freq):
        freq = str(freq)+'H'
        df= dataframe.groupby(pd.Grouper(freq=freq, origin='start')).count()
        df = df.reset_index()
        print(df)

        return df

    def calc_leastSquare(self,dataframe):
        dataframe['XY'] = dataframe['x'] * dataframe['y']
        dataframe['x2'] = dataframe['x']**2
        dataframe['y2'] = dataframe['y']**2
        dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
        #dataframe = dataframe.fillna(0)

        #print(dataframe)

        n = len(dataframe)
        sum_X = dataframe['x'].sum()
        sum_Y = dataframe['y'].sum()
        sum_XY = dataframe['XY'].sum()
        sum_x2 = dataframe['x2'].sum()
        sum_y2 = dataframe['y2'].sum()

        B = (n*sum_XY-sum_X*sum_Y)/(n*sum_x2-sum_X*sum_X)
        A = (sum_Y - B*sum_X)/(n)
        R = (n*sum_XY-sum_X*sum_Y)/math.sqrt((n*sum_x2-sum_X*sum_X)*(n*sum_y2-sum_Y*sum_Y))

        return B,A,R


    def calc_omori(self,dataframe,freq):
        dataframe['t'] = np.arange(len(dataframe))+1
        dataframe['x'] = dataframe['t']
        dataframe['y'] = 1/dataframe['count']

        B,A,R = self.calc_leastSquare(dataframe)
        a = 1/B
        b = A*a
        
        if b < 0:
            b = abs(b)
        if a < 0:
            a = abs(a)

        # hitung jika n(t) = 1
        # n(t) = a / (t + b)
        t = (a-b)/(24/freq)

        dataframe['calc_nt'] = a/(dataframe['t']+b)
    
        return [a,b,t,R],dataframe

    def calc_mogi1(self,dataframe,freq):
        dataframe['t'] = np.arange(len(dataframe))+1
        dataframe['x'] = np.log10(dataframe['t'])
        dataframe['y'] = np.log10(dataframe['count'])

        B,A,R = self.calc_leastSquare(dataframe)
        a = 10**A
        b = -B
        
        if b < 0:
            b = abs(b)

        # hitung jika n(t) = 1
        # n(t) = a.t^-b
        '''
        b log t = log a - log nt
        log t = (log a - log nt) / b
        t = 10 ^ (log a / b)
        '''
        t = (10**((np.log10(a))/b))
        t = t/(24/freq)

        dataframe['calc_nt'] = a*(dataframe['t']**(-b))
        
        return [a,b,t,R],dataframe

    def calc_mogi2(self,dataframe,freq):
        dataframe['t'] = np.arange(len(dataframe))+1
        dataframe['x'] = dataframe['t']
        dataframe['y'] = np.log(dataframe['count'])

        B,A,R = self.calc_leastSquare(dataframe)
        a = math.exp(A)
        b = -B

        if b < 0:
            b = abs(b)

        # hitung jika n(t) = 1
        # n(t) = a.e^-bt
        '''
        ln nt = ln a - bt
        t = (ln a)/b
        '''
        t = (np.log(a)/b)/(24/freq)
        dataframe['calc_nt'] = a*np.exp(-b*dataframe['t'])
        
        return [a,b,t,R],dataframe


    def calc_utsu(self,dataframe,freq):
        dataframe['t'] = np.arange(len(dataframe))+1
        dataframe['x'] = np.log10(dataframe['t']+0.01)
        dataframe['y'] = np.log10(dataframe['count'])

        B,A,R = self.calc_leastSquare(dataframe)
        a = 10**A
        b = -B

        if b < 0:
            b = abs(b)

        # hitung jika n(t) = 1
        # n(t) = a / (t + 0.01)^b
        '''
        log nt = log a - b log(t+0.01)
        log(t+0.01) = log a / b
        t = 10^(log a / b)- 0.01
        '''
        t = ((10**((np.log10(a))/b))-0.01)
        t = t/(24/freq)
        dataframe['calc_nt'] = a/((dataframe['t']+0.01)**b)
        
        return [a,b,t,R],dataframe

    def calc_nt(self,dataframe,freq,model_name,a_value,b_value):
        while dataframe['calc_nt'].iloc[-1]>self.limit and len(dataframe)<100*24/freq:
            OT = dataframe['OT'].iloc[-1] + timedelta(hours=freq)
            t = dataframe['t'].iloc[-1]+1
            
            if model_name == 'omori':
                calc_nt = a_value/(t+b_value)
            elif model_name == 'mogi_1':
                calc_nt = a_value*(t**(-b_value))
            elif model_name == 'mogi_2':
                calc_nt = a_value*np.exp(-b_value*t)
            elif model_name == 'utsu':
                calc_nt = a_value/(t+0.01)**b_value
                

            #print(model_name,t,calc_nt)

            dataframe = dataframe.append({'OT':OT,
                't':t,
                'calc_nt':calc_nt},
                ignore_index=True)

        dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
        dataframe = dataframe.fillna(0)
        dataframe.calc_nt=dataframe.calc_nt.mask(dataframe.calc_nt.lt(0),np.nan)
        dataframe.set_index('OT',inplace=True)

        return dataframe

    

    def pick_result(self,R_value,t_value,a_value,b_value):
        data = {
        'model':['Omori','Mogi_1','Mogi_2','Utsu'],
        'R_value':[abs(n) for n in R_value],
        't_value':t_value,
        'a_value':a_value,
        'b_value':b_value
        }
        df = pd.DataFrame(data)

        column = df['R_value']
        best_R = column.max()
        best_id = column.idxmax()
        best_model = df['model'][best_id]
        best_time = int(self.round_up(df['t_value'][best_id],0))
        best_a = df['a_value'][best_id]
        best_b = df['b_value'][best_id]
        
        return df