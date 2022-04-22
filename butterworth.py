import scipy
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("DA500.csv")

df = df[['velocity', 'time_of_day', 'Distance', 'SplitD']].copy()

#print(df)


x=df.time_of_day
y=df.velocity

   
# Sample rate and desired cutoff frequencies (in Hz).
order = 4
fs = 20
cut = 0.65

#apply filter, visually best fit is #filt2 or filt5. using filt2
sos = signal.butter(1,0.85, fs=20, output='sos')
filt = signal.sosfilt(sos, y)
df['Vfilt']=filt

sos = signal.butter(2,0.65, fs=20, output='sos')
filt2 = signal.sosfilt(sos, y)
df['Vfilt2']=filt2


fig = plt.figure()
ax = fig.subplots()
ax.plot(x,y, label ='original')
ax.plot(x,filt, label ='Vel filter')
ax.plot(x,filt2, label ='filt2')

ax.legend()
#plt.show()


fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
ax1.plot(x, y)
ax1.set_title('original2')
ax2.plot(x, filt2)
ax2.set_title('filter')
#plt.show()


