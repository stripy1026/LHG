import sys
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense
#from tensorflow.keras import optimizers




def makelog10( list ):
    loglist = []
    for i, k in enumerate( list ):
        loglist.append( math.log10( k ) )
    return loglist



def Avalanche_size_distribution_plot( ls, size, name ):

    lt = []
    for i in range( len(ls) ):
        if ls[i] != 0:
            lt.append( ls[i] )

    lsd = dict( zip( range( len(lt) ), lt ) )
    lsd_values = sorted(set(lsd.values()))
    lsdhist = [list(lsd.values()).count(i)/float( len(ls) ) for i in lsd_values]

    plt.plot(lsd_values,lsdhist, 'o', label='a = '+str( size ) )
    plt.title('Avalanche size Distribution of 2D lattice LHG model')
    plt.xlabel('Avalanche size s')
    plt.ylabel('P(s)')
    plt.xscale('log')
    plt.yscale('log')




if __name__ == '__main__':

    print( '==== Please enter [the name of data file] or [quit] to plot a graph. ====' )

    while True:

        Date = sys.stdin.readline().rstrip()

        if Date == 'quit':
            break

        dataframe1 = pd.read_csv( Date+'.csv' )

        Avalanche_size_distribution_plot( dataframe1['AC'], dataframe1['a'][1], Date )
        print( "done" )


    plt.show()
