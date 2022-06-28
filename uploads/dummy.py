'''
This is dummy file for testing purposes
'''

import os
import random
import string
try:
    from ._data_reader import DataReader
    from ._decay_calculator import DecayCalculator
    from ._data_plot import DoublePlot, show_plot, save_plot
except:
    from _data_reader import DataReader
    from _decay_calculator import DecayCalculator
    from _data_plot import DoublePlot, show_plot, save_plot


'''
CONSTANTA
'''
FILENAME ='_dummy_data'
FREQ = 24

_read = DataReader()
_df = _read._multi(FILENAME)

#print(_df)

app = DecayCalculator(dataframe=_df)
#print(decay)
_df = app.convert_time()
print(_df)

_df = app.freq_df(dataframe=_df,freq=FREQ)

print('calculating Omori')
omori, df_omori = app.calc_omori(dataframe=_df,freq=FREQ)

print('calculating Mogi 1')
mogi_1, df_mogi_1 = app.calc_mogi1(dataframe=_df,freq=FREQ)

print('calculating Mogi 2')
mogi_2, df_mogi_2 = app.calc_mogi2(dataframe=_df,freq=FREQ)

print('calculating Utsu')
utsu, df_utsu = app.calc_utsu(dataframe=_df,freq=FREQ)

model_name = ['omori','mogi_1','mogi_2','utsu']
data_set = [omori, mogi_1, mogi_2, utsu]
dataframe_set = [df_omori, df_mogi_1, df_mogi_2, df_utsu]