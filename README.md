Extract data from vbox Sport unit for data analysis in kayak sprint 

files are stored as text in a .vbo file

There are two files that extract data, 

get_data2.py which works as a basic script and now conatins the calculations for stroke rate and the butterworthg filters

readvbox2.py is an OOP script producing just the csv data and a basic matplotlib graph of speed.

Butterworth.py and SR.py have the example calculations tested before adding into get_data2

The webapp is underdevelopment in Django with a Plotly Dash app to take care of the interactive aspect required for the graphing visuals
This can be accessed through plotly_vbo2.py


vbox.py is the basis of this code available here. https://github.com/quentinsf/vboxutils


