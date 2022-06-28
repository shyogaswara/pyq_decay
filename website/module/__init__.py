#!/usr/bin/env python

''' The main module of PyQ Decay. Please refer to each module for more
detailed explanation.

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
'''
import copy
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

__author__ = 'Shandy Yogaswara'
__copyright__ = 'Copyright 2021, PyQ Decay Calculator'
__license__= 'GPL-3.0'
__version__ = '1.2.0'
__email__ = 'sh.yogaswara@gmail.com'
__status__ = 'Development'

def main(filename,frequency, save_folder):
    '''
    Read Raw Data
    '''
    
    _read = DataReader()
    _df = _read._multi(filename)
    
    '''
    Delete all data from save_folder
    '''
    images_files = os.listdir(save_folder)
    for images in images_files:
        if images.endswith('.png'):
            os.remove(os.path.join(save_folder,images))

    '''
    Calculating EQ Decay
    '''
    app = DecayCalculator(dataframe=_df)
    _convert_time = app.convert_time()
    frequency_df = app.freq_df(
        dataframe=_convert_time,
        freq=frequency
        )

    omori, df_omori = app.calc_omori(
        dataframe=frequency_df,
        freq=frequency
        )
    mogi_1, df_mogi_1 = app.calc_mogi1(
        dataframe=frequency_df,
        freq=frequency
        )
    mogi_2, df_mogi_2 = app.calc_mogi2(
        dataframe=frequency_df,
        freq=frequency
        )
    utsu, df_utsu = app.calc_utsu(
        dataframe=frequency_df,
        freq=frequency
        )

    R_value = [omori[3], mogi_1[3], mogi_2[3], utsu[3]]
    t_value = [omori[2], mogi_1[2], mogi_2[2], utsu[2]]
    a_value = [omori[0], mogi_1[0], mogi_2[0], utsu[0]]
    b_value = [omori[1], mogi_1[1], mogi_2[1], utsu[1]]
    model_name = ['omori','mogi_1','mogi_2','utsu']
    dataframe = [df_omori, df_mogi_1, df_mogi_2, df_utsu]

    #_result = app.pick_result(R_value,t_value,a_value,b_value)
    #print(_result)

    for i in range(len(dataframe)):
        print(i)
        _df_decay = app.calc_nt(
            dataframe=dataframe[i],
            freq=frequency,
            model_name=model_name[i],
            a_value=a_value[i],
            b_value=b_value[i]
            )
        print(_df_decay)
        plot = DoublePlot(
            _df_decay.index,
            _df_decay['calc_nt'],
            'Peluruhan',
            _df_decay['count'],
            'Real',
            'Waktu(WIB)'
            )
        plot.line_bar(title=model_name[i])
        _ascii_str = string.ascii_lowercase
        _random_str = ''.join(random.choice(_ascii_str) for i in range(4))
        path = os.path.join(
            save_folder,
            f'{model_name[i]}_{_random_str}.png'
            )
        save_plot(path)
        json_path = os.path.join(
            save_folder,
            f'{model_name[i]}.json')
        '''
        _json_res = _read.df2json(
            dataframe=_df_decay,
            filename=json_path
            )
        '''

        '''
        return image
        '''
    _image_list = os.listdir(save_folder)
    image_list = [image for image in _image_list]
    
    return image_list

    
    #show_plot()


if __name__ == '__main__':
    fname = 'test_data'
    freq = 3
    main(filename=fname,frequency=freq)




