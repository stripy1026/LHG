import sys
import random
import matplotlib.pyplot as plt
import pandas as pd

def Make_node_list( node_size, initial_value, graph_type ):

    if graph_type == 1: #complete graph

        node_list = [initial_value]*node_size

    return node_list

def Make_link_list( node_size, initial_value, graph_type ):

    if graph_type == 1: #complete directed graph

        link_list = list( [initial_value]*node_size for _ in range( node_size ) )

    return link_list

def Inject_current( node_list, node_size, external_current ):

    coordinate = random.randrange( 0, node_size )

    node_list[ coordinate ] += external_current

    return

def Recover_neurotransmitter( alpha, fraction, v, node_size, connection_strength ):

    connection_strength += ( (1/(v*node_size))*((alpha/fraction) - connection_strength ) )

    return connection_strength

def Avalanche_update( node_list, link_list, temp_node_list, temp_link_list, node_size, fraction ):

    avalanche_check_list = []
    changed = True

    while changed:

        changed = False

        for i in range( node_size ):

            if node_list[i] > 1:

                node_list[i] -= 1
                changed = True

                if not i in avalanche_check_list:

                    avalanche_check_list.append( i )

                neighbor_count = 0

                for nc in range( node_size ):

                    if link_list[i][nc]:

                        neighbor_count += 1

                for j in range( node_size ):

                    if link_list[i][j]:

                        temp_node_list[j] += (1/neighbor_count)*fraction*link_list[i][j]
                        temp_link_list[i][j] -= fraction*link_list[i][j]


        for i in range( node_size ):

            node_list[i] += temp_node_list[i]
            temp_node_list[i] = 0

            for j in range( node_size ):

                link_list[i][j] += temp_link_list[i][j]
                temp_link_list[i][j] = 0


    avalanche_count = len( avalanche_check_list )

    return avalanche_count


if __name__ == "__main__":

    # Set Parameters

    node_size = 300
    alpha = 1.4
    v = 10
    fraction = 0.2
    external_current = 0.025
    Avalanche_cycle = 1000

    ########################

    # Plot graph

    G_nodes = Make_node_list( node_size, 0, 1 )
    G_links = Make_link_list( node_size, (alpha/fraction), 1 )
    G_temp_nodes = Make_node_list( node_size, 0, 1 )
    G_temp_links = Make_link_list( node_size, 0, 1 )

    Avalanche_Datalist = []
    Avalanche_done_count = 0

    neuro_list = []
    neuros_list = []

    Number_of_links = 0
    for i in range( node_size ):

        for j in range( node_size ):

            if G_links[i][j]:

                Number_of_links += 1

    while Avalanche_done_count < Avalanche_cycle:

        Inject_current( G_nodes, node_size, external_current )

        avalanche_count = Avalanche_update( G_nodes, G_links, G_temp_nodes, G_temp_links, node_size, fraction )

        Avalanche_Datalist.append( avalanche_count )

        if avalanche_count:

            Avalanche_done_count += 1
            print( "Avalanche size : ", avalanche_count )
            print( "Avalanche count = ", Avalanche_done_count, "/", Avalanche_cycle )

        Total_neuro = 0
        one_neuro = 0

        for i in range( node_size ):

            for j in range( node_size ):

                G_links[i][j] = Recover_neurotransmitter( alpha, v, fraction, G_links[i][j], node_size )
                Total_neuro += G_links[i][j]
                
                if i == node_size//2 and j == node_size//2:

                    one_neuro += G_links[i][j]

        neuro_list.append( Total_neuro/Number_of_links )
        neuros_list.append( one_neuro )

   
    print( "==== Please enter the file name ====" )
    file_name = sys.stdin.readline().rstrip()

    dataframe1 = pd.DataFrame( { 'AC' : Avalanche_Datalist, 'a' : alpha, 'N' : neuro_list, 'NS' : neuros_list } )

    dataframe1.to_csv( file_name + ".csv" )