#!/usr/bin/env python
'''This code is used to create a choice of plot from predetermined axis 
from a dataframe.

The ReadData is used to read some file into dataframe
and determine the X and Y axis. ReadData in this module is not to be 
confused with DataReader from _data_reader module since they serve 
different purpose.

The SinglePlot and DoublePlot is used to generete single plot and 
double plot respectivelly'''

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

__author__ = 'Shandy Yogaswara'
__copyright__ = 'Copyright 2021, PyQ Decay Calculator'
__license__= 'GPL-3.0'
__version__ = '1.0.0'
__email__ = 'sh.yogaswara@gmail.com'
__status__ = 'Development'


class ReadData:
    '''
    this class used to read data from a file
    example to call this class is with
    
    ReadData(filename,separator,header)
    
    if using header or
    
    ReadData(filename,separator)
    
    if not using header. refer to line 240
    and line 242 for example
    '''
    def __init__(self,*args):
        '''
        get initial value from arguments
        which is filename, separator, and 
        header if true
        '''
        self.fname=args[0]
        self.sep=args[1]
        if len(args)>2:
            self.header=0
        else:
            self.header=None

    def read_data(self):
        '''read filename as pandas dataframe'''
        df = pd.read_csv(
            self.fname,
            sep=self.sep,
            engine='python',
            header=self.header)
        return df

    def deter_axis(self,dataframe,x_header,*y_header):
        '''
        get x and y axis value from dataframe.
        the code will try to save x axis value
        in datetime format
        y axis value will be saved in a list
        that can be called using list number like
        y_axis[0] or y_axis[1]
        '''
        try:
            dataframe[x_header]=pd.to_datetime(dataframe[x_header])
            x_axis=dataframe[x_header].strftime('%Y-%m-%d')
        except:
            x_axis=dataframe[x_header]
        y_axis=[]
        for y in y_header:
            y_axis.append(dataframe[y])

        return x_axis, y_axis


class SinglePlot:
    '''
    this class used to create plot
    to call this class, use

    SinglePlot(x_value,y_value,x_axisname,y_axisname)

    refer to line 247 at the end of classess for
    example
    '''
    def __init__(self, *args):
        '''
        create initial figure and axis
        from matplotlib with arguments
        as followed : x value, y value,
        x header name, and y header name
        the header name will refer to 
        x_axis and y_axis value just 
        like deter_axis function
        '''
        self.fig, self.ax=plt.subplots()
        self.x, self.y = args[0], args[1]
        self.x_header = args[2]
        self.y_header = args[3]

        '''
        the code below is initial config
        for plot like x label and y label
        also the autoscale. you may add
        some rotation on label here or
        another plot configuration as
        your need. please refer to
        matplotlib documentation
        '''
        self.ax.autoscale(tight=True)
        self.ax.set_xlabel(self.x_header)
        self.ax.set_ylabel(self.y_header)
        plt.tight_layout()

    def single_bar(self):
        '''create bar plot'''
        self.ax.bar(self.x,self.y)
        

    def single_line(self):
        '''create line plot'''
        self.ax.plot(self.x,self.y)

    def pie_chart(self):
        '''
        create pie chart. x value will be 
        used as label instead. not all data
        could be presented as pie chart like
        time series data, which better if
        presented as line plot or bar plot
        '''
        self.ax.pie(self.y, labels=self.x)
        plt.axis('off')

class DoublePlot:
    '''
    this class used to create multiple plot
    on same chart. to call this class, use

    MultiPlot(x_value,y1_value,y1_label,y2_value,y2_label,x_axisname)

    refer to line 249 at the end of classess for
    example
    '''
    def __init__(self, *args):
        '''
        create initial figure and axis
        from matplotlib with arguments
        as followed : x value, first y value
        and label, second y value and label
        and x axis name.
        '''
        self.fig, self.ax=plt.subplots()
        self.x = args[0]
        self.y1, self.label_y1 = args[1], args[2]
        self.y2, self.label_y2 = args[3], args[4]
        self.axis_name = args[5]

        '''
        the code below is initial config
        for plot like label and autoscale.
        you may add some rotation on label
        here or another plot configuration
        as you see fit. please refer to
        matplotlib documentation.
        as for legend, it cant be placed
        here because it need label value
        that declared in each function below
        '''
        self.ax.autoscale(tight=True)
        self.ax.set_xlabel(self.axis_name)
        

    def double_bar(self):
        '''
        create bar plot with double data
        each data will be separated by width
        value. if x axis consist of datetime
        format, the code will translate it
        to number for poisition purposes 
        and then re-translate it to datetime 
        format
        '''
        try:
            x = mdates.date2num(self.x)
        except:
            x=self.x
        width = 0.8
        self.ax.bar(x-width,self.y1,width,label=self.label_y1)
        self.ax.bar(x+width,self.y2,width,label=self.label_y2)
        self.ax.xaxis_date()
        self.ax.legend(loc='upper right')
        

    def double_line(self):
        '''create double line plot'''
        self.ax.plot(self.x,self.y1,label=self.label_y1)
        self.ax.plot(self.x,self.y2,label=self.label_y2)
        self.ax.legend(loc='upper right')
    
    def line_bar(self,title=None):
        '''
        create line plot for first dataset
        and bar plot for second dataset.
        refer first and second dataset 
        position explanation in MultiPlot
        init function
        '''
        try:
            x = mdates.date2num(self.x)
        except:
            x=self.x
        self.ax.plot(x,self.y1,label=self.label_y1,color='k')
        self.ax.bar(x,self.y2,label=self.label_y2,width=0.1,color='b')
        self.ax.legend(loc='upper right')
        self.ax.xaxis_date()
        

        if title:
            self.ax.set_title(title)

def show_plot():
    plt.show()

def save_plot(path):
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(path)


    


# the code below is used to trying this script
# you may refer to this if planning to import
# this code in your own project

if __name__ == '__main__':
    ################ CONFIG ##################
    # file name of data that want to be opened
    fname='test_data.csv'
    # separator that used in data, some general
    # separators are multiple spaces ('\s+'),
    # tab ('\t'), comma (','), and line ('|')
    # please refer to Regex for detailed info
    separator=r','
    # the occurence of header inside data.
    # header must be at the first line if true
    header=True
    # set the x and y axis from data to plot
    # if header False, use header number, if 
    # header True, use header name instead
    x_axis, y0_axis, y1_axis='Date', 'Close', 'Open'
    ##########################################

    if header:
        data = ReadData(fname,separator,header)
    else:
        data = ReadData(fname,separator)
    df = data.read_data()
    x,y = data.deter_axis(df,x_axis,y0_axis,y1_axis)
    print(x,y)
    
    #plot = SinglePlot(x,y[0],x_axis,y0_axis)
    #plot.single_line()
    plot = DoublePlot(x,y[0],y0_axis,y[1],y1_axis,x_axis)
    plot.line_bar()
    plt.show()