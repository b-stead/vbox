import collections
import csv
import re
import sys
import time
import datetime
import os
from pprint import pprint
import pandas as pd

#Variables
section = None
expected_fields = None
headers = []
column_names = []
bits = []
creation_midnight = []
midnight_timestamp = []
data =[]
vbox = r"vbox"
file = input("enter file name: ")

with open(file) as raw:

    for line in (raw.readlines()):
    # Start of new section
        m = re.match(r'\[([\s\w)]+)\]', line)
        if m is not None:
            section = m.group(1)

        else:
            # We're within a section
            #get column names and substitute special characters for dataframe
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
                columns.append('SplitD') # distance covered d= vel/ o.o5 convert to variable for Hz based on later models at 10Hz
                VBoxDataTuple = collections.namedtuple('VBoxDataTuple', columns)

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

                #convert time value as appears as HHMMSS.ss and append in new column
                tstamp = bits[1]
                (hrs, mins, secs) = int(tstamp[0:2]), int(tstamp[2:4]), float(tstamp[4:])
                time_of_day = 3600 * hrs + 60 * mins + secs
                fields.append(time_of_day)

                #get absolute time, needs fixing
                """
                #midnight_timestamp = time.mktime(creation_midnight, '%m/%d/%Y %I:%M %p').timetuple())
                #absolute_timestamp = midnight_timestamp + time_of_day
                #absolute_time = datetime.fromtimestamp(absolute_timestamp)
                absolute_timestamp = time_of_day
                absolute_time = datetime.mktime(absolute_timestamp)
                fields.append( absolute_time )
                fields.append( absolute_timestamp )
                #print(absolute_timestamp)
                """


                # And lat and long are in minutes, with west as positive
                # Convert to conventional degrees as lat_deg and long_deg
                fields.append( float(fields[2])/60.0 )
                fields.append( -1 * float(fields[3])/60.0 )

                #distance NB!!Remove hard coding of time interval to account for 10 or 20Hz measurement
                fields.append(float(fields[4])/3.6*0.05 )

                # If there's no GPS signal, we won't have absolute time.
                # We assume that time=000000.00 indicates the start of useful data.
                if fields[1] ==0.0:
                    data = []

                tup = VBoxDataTuple(*fields)
                data.append(tup)

    #convert tuple into DataFrame
    df = pd.DataFrame(data)
    df['Distance'] = df.SplitD.cumsum()
    df.to_csv('test.csv')

    # delete excess columns not required, NB!! recheck if adding other columns
    df = df.drop(df.columns[[0,2,3,5,6,7,8,9,10,11,12,13,15,16]], axis=1)

    #add cumulative time
    #df['SplitTime'] = df.time_of_day.diff()
    #df['SessionTime'] = df.SplitTime.cumsum()
       
print(df[:5])

