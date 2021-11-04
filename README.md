# pyq_decay
script to analyze EQ decay using python


PyQ Decay ver 1.0

A pythonic script to analyze EQ aftershock decay
using method of Omori (1894), Mogi (1962), and Utsu (1957)
that used worldwide, include in Indonesia by BMKG.

This folder contain the main.py script and test_data.txt 
that used as an example for data format. There's also 
conda_environment.yml included for people who use Anaconda
or Miniconda (recomended). The yml files contain packages
that used to run.

The script only run using python 3. 
line 145 is text data input to analyze that contain time
of EQ in YYYY-MM-DD HH:mm:ss format. line 146 is frequency 
in hours that will be used to analyze data.


HOW TO INSTALL PACKAGES
- for Anaconda / Miniconda user
in your terminal, make sure that this file exist by using ls
and then type :

conda env create -f conda_environment.yml

conda would create a virtual environment named py3 (as the
first line of conda_environment.yml)
to activate this environment, go to terminal and then type :

conda activate py3

- for pip
in your terminal, type :
pip install pandas
pip install numpy
pip install matplotlib

additionally, you may install cartopy with
pip install cartopy.
if you by any chance decide to not install cartopy
please disable line 15 and 16 by adding # at the very first character
if using python 3, use pip3 instead.
for additional information, please refer to their corresponding
website.



There're soo much thing that can be improved here that 
i plan to do in the near future.

Thank you, and sorry for any wrong spelling.

Best regards, 

Yogaswara
