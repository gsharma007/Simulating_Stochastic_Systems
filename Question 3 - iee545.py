waiting_avg = []
prob = []
Queue_level_avg = []
n = 100
for i in range(0,n):
    import pandas as pd
    import numpy as np
    
    Arrival = 0
    Arrival_times = [0]
    Arrival_times_adj = []
    for i in range(0,1000):
        Xi = np.random.exponential(scale = 0.7205)
        Arrival = Arrival + Xi
        Arrival_times.append(Arrival + Xi)
    for i in range(0, len(Arrival_times)):
        if Arrival_times[i] <= 480:
            Arrival_times_adj.append(Arrival_times[i])
    
    ##########################################################################################

    #Clerk 1 Service Times
    Clerk1_Service = []
    for i in range(0,len(Arrival_times_adj)):
        X = np.random.exponential(scale = 4.81)
        Clerk1_Service.append(X)
    
    #########################################################################################
    
    #SIMULATION OF THE SYSTEM - BANK OF AMERICA
    Dep_clerk1 = []
    
    if Arrival_times_adj[0] == 0:
        Dep_clerk1.append(Clerk1_Service[0])
    else:
        Dep_clerk1.append(Arrival_times_adj[0] + Clerk1_Service[0])
    
   
    for i in range(1, len(Arrival_times_adj)):
        if Dep_clerk1[i-1] > Arrival_times_adj[i]:
            Dep_clerk1.append(Dep_clerk1[i-1] + Clerk1_Service[i])
        else:
            Dep_clerk1.append(Arrival_times_adj[i] + Clerk1_Service[i])

    ############################################################################################
    
    wait_time1 = []
    
    for i in range(0, len(Arrival_times_adj)):
        wait_time = Dep_clerk1[i] - Arrival_times_adj[i] - Clerk1_Service[i]
        wait_time1.append(wait_time)
        
    np.mean(wait_time1)
    #################################

    waiting_avg.append(np.mean(wait_time1))
    ################################

    Queue_level1 = []
    Event_time1 = []
    S1 = 1
    Q1 = 0
    i = 0
    j = 0
    x = len(Arrival_clerk1)
    y = len(Dep_clerk1)
    while i <= x - 1 and j <= y - 1:
        if Arrival_clerk1[i] < Dep_clerk1[j]:
            Event_time1.append(Arrival_clerk1[i])
            if S1 == 0:
                Q1 = Q1 + 1
            else:
                S1 = S1 - 1
            i = i + 1
            Queue_level1.append(Q1)
        
        else:
            Event_time1.append(Dep_clerk1[j])
            if Q1 > 0:
                Q1 = Q1 - 1
            else:
                S1 = S1 + 1
            j = j + 1
            Queue_level1.append(Q1)
            
    mean_q1 = np.mean(Queue_level1)
     
    ###
    
    Queue_level2 = []
    Event_time2 = []
    S2 = 1
    Q2 = 0
    i = 0
    j = 0
    x = len(Arrival_clerk2)
    y = len(Dep_clerk2)
    while i <= x - 1 and j <= y - 1:
        if Arrival_clerk2[i] < Dep_clerk2[j]:
            Event_time2.append(Arrival_clerk2[i])
            if S2 == 0:
                Q2 = Q2 + 1
            else:
                S2 = S2 - 1
            i = i + 1
            Queue_level2.append(Q2)
        
        else:
            Event_time2.append(Dep_clerk2[j])
            if Q2 > 0:
                Q2 = Q2 - 1
            else:
                S2 = S2 + 1
            j = j + 1
            Queue_level2.append(Q2)
            
    mean_q2 = np.mean(Queue_level2)   
    
    ###
    
    Queue_level3 = []
    Event_time3 = []
    S3 = 1
    Q3 = 0
    i = 0
    j = 0
    x = len(Arrival_clerk3)
    y = len(Dep_clerk3)
    while i <= x - 1 and j <= y - 1:
        if Arrival_clerk3[i] < Dep_clerk3[j]:
            Event_time3.append(Arrival_clerk3[i])
            if S3 == 0:
                Q3 = Q3 + 1
            else:
                S3 = S3 - 1
            i = i + 1
            Queue_level3.append(Q3)
        
        else:
            Event_time3.append(Dep_clerk3[j])
            if Q3 > 0:
                Q3 = Q3 - 1
            else:
                S3 = S3 + 1
            j = j + 1
            Queue_level3.append(Q3)
            
    mean_q3 = np.mean(Queue_level3) 
    Queue_level_avg.append(np.mean([mean_q1, mean_q2, mean_q3]))
    
    
    
print("Mean wait time",np.mean(waiting_avg))
print("Mean of Probability",np.mean(prob))
    
print("STD wait time",np.std(waiting_avg))
print("STD of Probability",np.std(prob))
    
#Confidence Intervals:
from scipy import stats
t = stats.t.ppf(1-0.025,n)
    
#half_width_wait_time = t*(1.025/np.sqrt(n)) 
#print(half_width_wait_time)

half_width_probability = t*(np.std(prob)/np.sqrt(n))
print("Half width probability", half_width_probability)

#################################

print("Mean Queue level", np.mean(Queue_level_avg))
print("STD Queue level", np.std(Queue_level_avg))


np.savetxt('kck.txt', waiting_avg, delimiter = '\t')
