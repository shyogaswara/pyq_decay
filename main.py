##########################################################################
# By : Shandy Yogaswara                                                  #
# email : sh.yogaswara@gmail.com                                         #
##########################################################################
# this is earlier version of EQ Decay Analysis With Python, or Pyq_Decay #
# the script inspired by EQ Decay analysis tool used by BMKG, Indonesia  #
# with purposes to calculate when the EQ Aftershock will be over.        #
# Their script use Matlab, which cannot run properly on my machine       #
# so i decide to replicate it using python.                              #
# i have plan to create a GUI for this one in the near future.           #
# but please don't hestitate to use this script.                         #
##########################################################################

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import io
import matplotlib.colors as colors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import math


class app_peluruhan:
	def __init__(self,file_name):
		self.df = pd.read_csv(file_name,engine='python',header=None)
		self.df.columns = ['count']

	def convert_time(self):
		#self.df['OT'] = self.df['date']+' '+self.df['hours']
		self.df['OT'] = pd.to_datetime(self.df['count'])
		self.df.set_index('OT',inplace=True)

		return self.df

	def round_up(self,n,decimals):
		multiplier = 10**decimals
		return math.ceil(n * multiplier) / multiplier

	def round_down(self,n,decimals):
		multiplier = 10**decimals
		return math.floor(n * multiplier) / multiplier


	def freq_df(self,dataframe,freq):
		freq = str(freq)+'H'
		df= dataframe.groupby(pd.Grouper(freq=freq)).count()

		return df

	def calc_leastSquare(self,dataframe):
		dataframe['XY'] = dataframe['x'] * dataframe['y']
		dataframe['x2'] = dataframe['x']**2
		dataframe['y2'] = dataframe['y']**2
		dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
		dataframe = dataframe.fillna(0)

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
		dataframe['x'] = np.arange(len(dataframe))+1
		dataframe['y'] = 1/dataframe['count']
		
		B,A,R = app.calc_leastSquare(dataframe)
		a = 1/B
		b = A*a 

		# hitung jika n(t) = 1
		t = (a-b)/(24/freq)

		return t, R

	def calc_mogi1(self,dataframe,freq):
		dataframe['x'] = np.log10(np.arange(len(dataframe))+1)
		dataframe['y'] = np.log10(dataframe['count'])

		B,A,R = app.calc_leastSquare(dataframe)
		a = 10**A
		b = -B

		# hitung jika n(t) = 1
		t = (a-b)/(24/freq)

		return t, R

	def calc_mogi2(self,dataframe,freq):
		dataframe['x'] = np.arange(len(dataframe))+1
		dataframe['y'] = np.log(dataframe['count'])

		B,A,R = app.calc_leastSquare(dataframe)
		a = math.exp(A)
		b = -B

		# hitung jika n(t) = 1
		t = (a-b)/(24/freq)

		return t, R


	def calc_utsu(self,dataframe,freq):
		dataframe['x'] = np.log10((np.arange(len(dataframe))+1)+0.01)
		dataframe['y'] = np.log10(dataframe['count'])

		B,A,R = app.calc_leastSquare(dataframe)
		a = 10**A
		b = -B

		# hitung jika n(t) = 1
		t = (a-b)/(24/freq)

		return t, R

	def pick_result(self,R_value,t_value):
		data = {'model':['Omori','Mogi 1','Mogi 2','Utsu'], 'R_value':[abs(n) for n in R_value], 't_value':t_value}
		df = pd.DataFrame(data)

		column = df['R_value']
		best_R = column.max()
		best_id = column.idxmax()
		best_model = df['model'][best_id]
		best_time = int(app.round_up(df['t_value'][best_id],0))
		
		return(f'model terpilih adalah {best_model} dengan nilai R sebesar {best_R}, yang mana kejadian gempabumi akan berakhir setelah hari ke-{best_time}') 



if __name__ == '__main__':
	
	file_name = 'test_data.txt'
	freq = 3
	# the freq here is frequency for data to be readed by hour.
	# ex, 3 here mean the data would be counted for each 3 hours.
	# if u want to analyze using daily frequency, use 24 for 1 day
	
	app = app_peluruhan(file_name)
	convert_time = app.convert_time()
	freq_df = app.freq_df(convert_time,freq)
	omori, omori_R = app.calc_omori(freq_df, freq)
	mogi_1, mogi_1R = app.calc_mogi1(freq_df, freq)
	mogi_2, mogi_2R = app.calc_mogi2(freq_df, freq)
	utsu, utsu_R = app.calc_utsu(freq_df, freq)
	R_value = [omori_R, mogi_1R, mogi_2R, utsu_R]
	t_value = [omori, mogi_1, mogi_2, utsu]
	result = app.pick_result(R_value,t_value)
	print(result)
