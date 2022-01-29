# Extrct data from file in format .VBO, format for dataframe and convert to csv

import collections
import csv
import json
from pkgutil import get_data
import re
import sys
import time
from datetime import datetime
import os
import pandas as pd
from pprint import pprint
import csv

class VBox(object):



    def __init__(self, filename):
        self.filename = filename
        self.creation_date = None
        self.creation_midnight = None
        self.comments = []
        self.headers = []
        self.column_names = []
        self.data = []
        
        #extract data from doc by sections, convert lat/long from minutes into degrees
    def get_data(self):
        section = None
        expected_fields = None

        with open(self.filename) as raw:

            for line in (raw.readlines()):
            # Start of new section
                m = re.match(r'\[([\s\w)]+)\]', line)
                if m is not None:
                    section = m.group(1) 

                    # get data by section headers
                else:
                    if line and (section == 'column names'):
                        column_names = line.split()
                        columns = [re.sub("[\-. ]","_",x) for x in column_names]
                        columns.remove('vo')
                        column_name_map = dict([k[::-1] for k in enumerate(columns)])
                        assert(columns[1] == 'time')  # We assume this later
                        assert(columns[2] == 'lat')   # We assume this later
                        assert(columns[3] == 'long')  # We assume this later
                        columns.append('time_of_day') # time converted into secs
                        #columns.append('datetime')    # absolute time add in when fixed absulute time section
                        #columns.append('timestamp')   # absolute time in secs
                        columns.append('lat_deg')     # latitude in degrees
                        columns.append('long_deg')    # longitude in degrees
                        columns.append('distance')     # distance covered d= vel/ o.o5 need to check assumptions maybe better with positional co-ordinates and accelerometer data
                        VBoxDataTuple = collections.namedtuple('VBoxDataTuple', columns)

                            #print(columns)
                            #print(VBoxDataTuple)        
        
                    #seperate values in lines with data
                    if line and (section == 'data'):
                        bits = line.split()
                
                    # Check we got the number of fields we expected - the last line
                    # can sometimes be truncated.
                    #if expected_fields is None:
                        #expected_fields=len(bits)
                    #if len(bits) != expected_fields:
                        #log.warning('Skipping a data line which does not include %s fields', expected_fields)
                        #continue
                    
                        fields = [float(f) for f in bits]

                        # Time, however, looks like a float but is HHMMSS.SS
                        tstamp = bits[1]
                        (hrs, mins, secs) = int(tstamp[0:2]), int(tstamp[2:4]), float(tstamp[4:])
                        # Add a new field with the time in seconds from midnight
                        time_of_day = 3600 * hrs + 60 * mins + secs
                        fields.append(time_of_day)
                        # We turn it into an absolute timestamp by offsetting the time
                        # needs fixing
                        """
                        midnight_timestamp = time.mktime(self.creation_midnight.timetuple())
                        absolute_timestamp = midnight_timestamp + time_of_day
                        absolute_time = datetime.fromtimestamp(absolute_timestamp)
                        fields.append( absolute_time )
                        fields.append( absolute_timestamp )"""
                        
                        # And lat and long are in minutes, with west as positive
                        # Convert to conventional degrees as lat_deg and long_deg
                        fields.append( float(fields[2])/60.0 )
                        fields.append( -1 * float(fields[3])/60.0 )

                        #elapsed time


                        #distance
                        fields.append( float(fields[4])*0.05)

                        # If there's no GPS signal, we won't have absolute time.
                        # We assume that time=000000.00 indicates the start of useful data.
                        # (This comes from an early test file where the first few records
                        # were at 23:59:xx.xxx.)"""
                        if fields[1] == 0.0:
                            self.data = []
        
                        tup = VBoxDataTuple(*fields)
                        self.data.append(tup)
                        #print(tup)
            df = pd.DataFrame(self.data)
            
            #print(df)

        #convert df to CSV
        df.to_csv('test.csv', index=False)           


    # create graph of data for velocity over time
    def get_graph(self):
      from matplotlib import pyplot as plt
      import numpy as np

      dataframe = pd.read_csv(self.filename)

      x = dataframe.time_of_day
      y = dataframe.velocity


      plt.scatter(x,y)
      plt.show()


c = VBox('DA500.vbo')
a = c.get_data()

b = VBox('test.csv')
d = b.get_graph()



