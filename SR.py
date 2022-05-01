from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from butterworth import df
import os
#df = pd.read_csv("DA500.csv")

df2 = df[['velocity', 'time_of_day', 'Distance','Vfilt2', 'SplitD']].copy()
x=df2.Distance
y=df2.Vfilt2
v=df2.Vfilt2

#Find peaks
peaks = find_peaks(y, height=0)
height = peaks[1]['peak_heights'] #list of the heights of the peaks
peak_pos = x[peaks[0]] #list of the peaks positions

#Finding the minima as stroke start is at lowest point i.e. trough phase
yneg = y*-1
minima = find_peaks(yneg)
min_height = yneg[minima[0]] #list of the mirrored minima heights
#minima_height = minima[1]['peak_heights']
min_pos = x[minima[0]] #list of the minima positions

#Plotting minima
fig = plt.figure()
ax = fig.subplots()
ax.scatter(x,y)
ax.scatter(peak_pos, height, color = 'r', s = 15, marker = 'x', label = 'Maxima')
ax.scatter(min_pos, min_height*-1, color = 'gold', s = 15, marker = 'X', label = 'Minima')
ax.legend()
ax.grid()
plt.show()

#concat min_pos& min_height into dataframe
#add stroke position back onto df values

s=pd.concat([min_height, min_pos], axis=1)
s=s.rename(columns = {'Distance' : 'stroke'})
s['count'] = s.groupby('stroke').cumcount() +1
s.pop('Vfilt2')

#add time values onto s for calculations
time=df2.filter(['time_of_day'])
s=s.join(time)

#time diff between strokes, convert to stroke/min
s['time_diff'] = s['time_of_day'].diff()
s['Str_Rate']=60/s['time_diff']

#rolling average for SR windows of 3
s['SRMean3'] = s['Str_Rate'].rolling(3).mean()
s.pop('time_of_day')

df3=df2.join(s)
df3['count']=df3['count'].fillna(0)
df3['boolean'] = df3['count'].astype('bool')
#df3['SRMean3']= df3['SRMean3'].fillna(0)

#graph - Mean of window 3 provides a better visual fit
SR = df3.Str_Rate
SRM3 = df3.SRMean3

#remove points out of range
x2=x[SR>0]
SRa = SR[SR>0]

x3=x[SRM3>0]
SR3 = SRM3[SRM3>0]

plt.plot(x2,SRa, label='SR')
plt.plot(x3,SR3, label='SR3')
plt.legend()
plt.show()

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Distance (m)')
ax1.set_ylabel('Speed (Kph)', color=color)
ax1.plot(x,y, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Str/Min', color=color)
ax2.plot(x3,SR3, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.show()

#move df to csv
df4=df3[['velocity', 'Distance', 'Vfilt2', 'SRMean3', 'SplitD']]
os.makedirs('folder/subfolder', exist_ok=True)  
df4.to_csv('folder/subfolder/df4.csv')



