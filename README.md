Extract data from vbox Sport unit for data analysis in kayak sprint 

files are stored as text in a .vbo file

There are two files that extract data, 
get_data.py which works as a basic script,
readvbox2.py is an OOP script which is now also working

The Data filtering for velocity and stroke rate are taken care of in the following files 
butterworth.py SR.py
Next steps are to add these into the main script once filtering is checked for it's accuracy and fit.

The webapp is underdevelopment in Django with a Plotly Dash app to take care of the interactive aspect required for the graphing visuals
This can be accessed through plotly_vbo2.py


vbox.py is the basis of this code available here. https://github.com/quentinsf/vboxutils


