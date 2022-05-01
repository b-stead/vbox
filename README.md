Extract data from vbox Sport unit for data analysis in kayak sprint 

files are stored as text in a .vbo file

There are two files that extract data, 

get_data2.py which now conatins the calculations for stroke rate and the butterworth filters

readvbox2.py producing just the csv data and a basic matplotlib graph of speed.

Butterworth.py and SR.py have the example calculations tested before adding into get_data2

The webapp is underdevelopment in Django with a Plotly Dash app to take care of the interactive aspect required for the graphing visuals
This can be accessed through plotly_vbo2.py

Test sample file is DA500.vbo which can be passed in when prompted after executing python3 get_data2.py

vbox.py is the basis of this code available here. https://github.com/quentinsf/vboxutils


