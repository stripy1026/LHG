import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
from tqdm import tqdm


def Make_neuron_attributes_dict( init_value ):

    key = G.nodes
    val = [init_value]*len( G.nodes )

    node_attributes_dictionary = dict( zip( key, val ) )

    return node_attributes_dictionary


def Make_synapse_attributes_dict( alpha, fraction ):

    key = G.edges
    val = [ (alpha/fraction) ]*len( G.edges )

    edge_attributes_dictionary = dict( zip( key, val ) )

    return edge_attributes_dictionary


def Injects_current_to_2D_random( node_grid, size, amount ):

    i = random.randrange( 0, size )
    j = random.randrange( 0, size )

    node_grid[( i, j )] += amount


def Injects_current_to_random( node_grid, size, amount ):

    i = random.randrange( 0, size )

    node_grid[i] += amount


def Synaptic_dynamics( temp_grid, node_grid, edge_grid, fraction ):

    avalanche_count = 0

    for i, key in enumerate( node_grid ):

        if node_grid[ key ] > 1:

            changed = True
            node_grid[ key ] -= 1

            if Avalanche_grid[ key ] == 0:

                Avalanche_grid[ key ] = 1
                avalanche_count += 1
               
            neighbor_count = len( G[key] )

            for i, nbnode in enumerate( G[key] ):

                temp_grid[nbnode] += (1/neighbor_count)*fraction*edge_grid[( key, nbnode )]
                edge_grid[( key, nbnode )] -= fraction*edge_grid[( key, nbnode )]

    for i, key in enumerate( node_grid ):

        node_grid[ key ] += temp_grid[ key ]
        temp_grid[ key ] = 0


    return avalanche_count


def Recover_neurotransmitter( alpha, v, fraction, connection_strength, size ):

    connection_strength += ( 1/(v*size) )*( (alpha/fraction) - connection_strength )

    return connection_strength


if __name__ == '__main__':


    #==========================================================================

    # Set Parameters

    node_size = 100
    alpha = 1.4
    v = 10
    fraction = 0.2
    external_current = 0.025
    avalanche_cycle = 100

    #==========================================================================

    # Plot graph
    #G = nx.grid_2d_graph( 10, 10, create_using=nx.DiGraph() )
    G = nx.complete_graph( node_size, nx.DiGraph() )

    # This graph G be used to be a framework of the neuronal network.
    # I will use the attributes dictionary to simulate synaptic dynamics, while graph G remains still


    # Simulation


    A = Make_neuron_attributes_dict(0)
    B = Make_synapse_attributes_dict( alpha, fraction )
    C = Make_neuron_attributes_dict(0)

    Avalanche_Datalist = []
    Avalanche_done_count = 0

    timescale = 0
    timescale_list = []
    neuro_list = []
    neuros_list = []

    while Avalanche_done_count < avalanche_cycle:

        timescale += 1
        timescale_list.append( timescale )
        avalanche_count = 0
        Avalanche_grid = Make_neuron_attributes_dict(0)
        changed = True

        Injects_current_to_random( A, node_size, external_current )

        while changed:

            changed = False

            # J restoration term

            Total_neuro = 0
            one_neuro = 0

            for i, key in enumerate( B ):

                B[key] = Recover_neurotransmitter( alpha, v, fraction, B[key], node_size )
                Total_neuro += B[key]

                if i == 0:

                    one_neuro += B[key]

            # J term ends here.

            tmp_count = Synaptic_dynamics( C, A, B, fraction )
            avalanche_count += tmp_count

            if tmp_count:

                changed = True

        
        Avalanche_Datalist.append( avalanche_count )

        if avalanche_count:

            Avalanche_done_count += 1
            print( "Size : %d" %(avalanche_count) )
            print( 'Avalanche count = ', Avalanche_done_count, '/', avalanche_cycle )

        div = 0

        for i, key in enumerate( B ):

            div += 1

        neuro_list.append( Total_neuro/div )
        neuros_list.append( one_neuro )
       

    print( '==== Please enter the simulation date ====' )
    Date = sys.stdin.readline().rstrip()

    dataframe1 = pd.DataFrame( { 'AC' : Avalanche_Datalist, 'a' : alpha,
                                'T' : timescale_list, 'N' : neuro_list, 'NS' : neuros_list } )
    dataframe1.to_csv( Date+'.csv' )


    #==========================================================================

    # Draw graph


    nx.set_node_attributes( G, A, 'potential' )
    nx.set_edge_attributes( G, B, 'strength' )


    #pos = nx.spring_layout( G )

    #nx.draw( G, pos = pos, with_labels = False )

    lab1 = nx.get_node_attributes( G, 'potential' )
    lab2 = nx.get_edge_attributes( G, 'strength' )


    #for key in lab1:
    #    lab1[key] = round( lab1[key], 3 )

    #for key in lab2:
    #    lab2[key] = round( lab2[key], 3 )

#    for key in lab3:
#        lab3[key] = round( lab3[key], 3 )

    #nx.draw_networkx_labels( G, pos, labels = lab1 )
    #nx.draw_networkx_edge_labels( G, pos, edge_labels = lab2 )
#    nx.draw_networkx_edge_labels( G, pos, edge_labels = lab3 )

    #plt.show()