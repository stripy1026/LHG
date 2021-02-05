import sys
import pandas as pd
import matplotlib.pyplot as plt


print( "Please insert the file name." )
Date = sys.stdin.readline()


dataframe1 = pd.read_csv( Date+".csv" )

x = dataframe1['T']
y = dataframe1['N']
y2 = dataframe1['NS']
y3 = dataframe1['AC']


div = 0
for i in range( 300 ):
    div += i


plt.plot( y, '--', label = Date )
plt.plot( y2, label = Date+' spcf' )
plt.title( "Neurotransmitter" )
plt.xlabel( "Time(s)" )
plt.ylabel( "Amount" )


plt.legend()
plt.show()

plt.plot( y3 )
plt.show()
