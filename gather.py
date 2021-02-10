import sys
import pandas as pd


print( "Insert initial file name." )
input = sys.stdin.readline().rstrip()
if input == "quit":
    quit()

dataframe1 = pd.read_csv( input+".csv" )

while True:

    print( "Insert file name." )
    input = sys.stdin.readline().rstrip()

    if input == "quit":
        print( "Insert new file name." )
        fn = sys.stdin.readline().rstrip()
        dataframe1.to_csv( fn+".csv" )
        break

    dataframe2 = pd.read_csv( input+".csv" )
    result = pd.concat( [dataframe1,dataframe2], ignore_index = True )
    dataframe1 = result
    


