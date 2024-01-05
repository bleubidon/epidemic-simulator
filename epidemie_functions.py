import random as rd
import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
from time import time
import json
#import os; os.chdir('C:\\Users\\user\\Desktop\\path')

def write_to_file(list, fname='plot_lists.json', mode='a'):
    if mode == 'a':
        with open(fname, 'a') as f:
            json.dump(list, f)
            f.close()
    elif mode == 'w':
        with open(fname, 'w') as f:
            json.dump(list, f)
            f.close()

def disp_in_col(G):
    for i in G:
        print(i)
        
def moy_list(L):
    return sum(L)/float(len(L))

def grille(n):
    return [[0]*n for i in range(n)]

def init(n):
    grid = grille(n)
    infected_box_row, infected_box_col = rd.randrange(n), rd.randrange(n)
    grid[infected_box_row][infected_box_col] = 1
    return grid

def compte(G):
    dim = len(G)
    compte_list = [0,0,0,0]
    for i in G:
        for j in i:
            compte_list[j]+=1
    return compte_list
    
    
def est_exposee(G, i, j):
    n= len(G)
    if i == 0 and j == 0:
        return (G[0][1]-1)*(G[1][1]-1)*(G[1][0]-1) == 0
    elif i == 0 and j == n-1:
        return (G[0][n-2]-1)*(G[1][n-2]-1)*(G[1][n-1]-1) == 0
    elif i == n-1 and j == 0:
        return (G[n-1][1]-1)*(G[n-2][1]-1)*(G[n-2][0]-1) == 0
    elif i == n-1 and j == n-1:
        return (G[n-1][n-2]-1)*(G[n-2][n-2]-1)*(G[n-2][n-1]-1) == 0
    elif i == 0:
        return (G[0][j-1]-1)*(G[1][j-1]-1)*(G[1][j]-1)*(G[1][j+1]-1)*(G[0][j+1]-1) == 0
    elif i == n-1:
        return (G[n-1][j-1]-1)*(G[n-2][j-1]-1)*(G[n-2][j]-1)*(G[n-2][j+1]-1)*(G[n-1][j+1]-1) == 0
    elif j == 0:
        return (G[i-1][0]-1)*(G[i-1][1]-1)*(G[i][1]-1)*(G[i+1][1]-1)*(G[i+1][0]-1) == 0
    elif j == n-1:
        return (G[i-1][n-1]-1)*(G[i-1][n-2]-1)*(G[i][n-2]-1)*(G[i+1][n-2]-1)*(G[i+1][n-1]-1) == 0
    else:
        return (G[i][j-1]-1)*(G[i][j+1]-1)*(G[i-1][j]-1)*(G[i+1][j]-1)*(G[i-1][j-1]-1)*(G[i-1][j+1]-1)*(G[i+1][j+1]-1)*(G[i+1][j-1]-1) == 0
    
def bernoulli(p):
    x = rd.random()
    return int(x <= p)
    
def suivant(G, p1, p2):
    G_temp = deepcopy(G)
    n = len(G_temp)
    for i in range(n):
        for j in range(n):
            if G_temp[i][j] == 0 and est_exposee(G_temp, i, j) and bernoulli(p2):
                G_temp[i][j] = 1
            elif G_temp[i][j] == 1:
                if bernoulli(p1):
                    G_temp[i][j] = 3
                else:
                    G_temp[i][j] = 2
    return G_temp
    
def simulation(n, p1, p2):
    G = init(n)
    continue_ = True
    while continue_:
        G = suivant(G, p1, p2)
        continue_= False
        for i in G:
            if 1 in i:
                continue_ = True
                break
    return compte(G)

def stats(n, p1, p2min, p2max, p2step, nbr_simul):
    output_obj = []
    bilan_list, x_atteinte_list = [], []
    
    p2list = np.arange(p2min, p2max+p2step, p2step)
    p2list = [float(i) for i in p2list]
    
    output_obj.append(p2list)
    
    number_of_laps_total = len(p2list); number_of_laps_done = 0
    sub_progress_old = 0
    
    for i in p2list:
        print('\nProgress : {}/{}; {}% '.format(number_of_laps_done, number_of_laps_total, round(100*number_of_laps_done/number_of_laps_total)), end='')    
        number_of_sim_total = nbr_simul; number_of_sim_done = 0
        
        results_list= []
        list0, list1, list2, list3 = [], [],[], []
        for j in range(nbr_simul):
            results_list.append(simulation(n, p1, i))
            
            number_of_sim_done += 1
            sub_progress = int(100*(number_of_sim_done/number_of_sim_total))
            if sub_progress != sub_progress_old:
                print('=', end='')
            
        for j in range(len(results_list)):
            list0.append(results_list[j][0])
            list1.append(results_list[j][1])
            list2.append(results_list[j][2])
            list3.append(results_list[j][3])
        
        moy_list0 = moy_list(list0)
        moy_list1 = moy_list(list1)
        moy_list2 = moy_list(list2)
        moy_list3 = moy_list(list3)
        
        bilan_list.append([moy_list0,moy_list1,moy_list2,moy_list3])
        
        var = (bilan_list[-1][2] + bilan_list[-1][3])/n**2
        x_atteinte_list.append(var)
        number_of_laps_done += 1

    output_obj.append(x_atteinte_list)
    write_to_file(output_obj, mode ='w' )


    return x_atteinte_list, p2list
        
def plot_stats(x_atteinte_list, p2list):
    plt.grid()
    plt.axis([min(p2list), max(p2list), min(x_atteinte_list), max(x_atteinte_list)])
    plt.title('Proportion de la population atteinte en fonction de p2')
    plt.xlabel('p2')
    plt.ylabel('Proportion de la population atteinte')
    plt.plot(p2list, x_atteinte_list)
    plt.show(block=True)
    
#Static parameters
p1 = .5
p2min = 0
p2max = 1

#Custom parameters
n = 10
p2step = .1
nbr_simul = 200

start_time = time()
#x_atteinte_list, p2list = stats(n, p1, p2min, p2max, p2step, nbr_simul)

print('\n\nCompleted 100%')
print('Duration : {} sec(s)'.format(round(time()-start_time, 2)))

#plot_stats(x_atteinte_list, p2list)
