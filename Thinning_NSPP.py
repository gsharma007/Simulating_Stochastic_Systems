# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 19:16:54 2018

@author: kkeezhna
"""

waiting_avg = []
prob = []
n = 400
for i in range(0,n):
    import pandas as pd
    import numpy as np
    
    Arrival = 0
    Arrival_times = []
    
    for i in range(0,100):
        An = np.random.exponential(scale = 6.667)
        Arrival = Arrival + An
        Arrival_times.append(Arrival)
    Arrival_NSPP1 = [0]
    Arrival_NSPP = []
    
    for i in range(0,100):
        U = np.random.uniform()
        if Arrival_times[i] >= 0 and Arrival_times[i] < 48:
            lamda = 0.15
        elif Arrival_times[i] >= 48 and Arrival_times[i] < 96:
            lamda = 0.1604
        elif Arrival_times[i] >= 96 and Arrival_times[i] < 144:
            lamda = 0.1417
        elif Arrival_times[i] >= 144 and Arrival_times[i] < 192:
            lamda = 0.1292  
        elif Arrival_times[i] >= 192 and Arrival_times[i] < 240:
            lamda = 0.1458
        elif Arrival_times[i] >= 240 and Arrival_times[i] < 288:
            lamda = 0.1146
        elif Arrival_times[i] >= 288 and Arrival_times[i] < 336:
            lamda = 0.1313
        elif Arrival_times[i] >= 336 and Arrival_times[i] < 384:
            lamda = 0.15
        elif Arrival_times[i] >= 384 and Arrival_times[i] < 432:
            lamda = 0.1313
        elif Arrival_times[i] >= 432 and Arrival_times[i] < 480:
            lamda = 0.1416       
        
        ratio = lamda/0.1604
        if U <= ratio:
            Arrival_NSPP1.append(Arrival_times[i])
    
    for i in range(0, len(Arrival_NSPP1)):
        if Arrival_NSPP1[i] <= 480:
            Arrival_NSPP.append(Arrival_NSPP1[i])
                 
    Interarrival_NSPP = []
    for i in range(0, len(Arrival_NSPP) - 1):
        K = Arrival_NSPP[i+1] - Arrival_NSPP[i]
        Interarrival_NSPP.append(K)
    
    ##########################################################################################
    
    dataset1 = pd.read_csv("C1service.csv")
    dataset2 = pd.read_csv("C2service.csv") 
    dataset3 = pd.read_csv("C3service.csv")  
    
    Clerk_1 = dataset1.iloc[:, 0].values
    Clerk_1 = list(Clerk_1)
    Clerk_2 = dataset2.iloc[:, 0].values
    Clerk_2 = list(Clerk_2)
    Clerk_3 = dataset3.iloc[:, 0].values
    Clerk_3 = list(Clerk_3)
    
    #Clerk 1 Service Times
    Clerk1_Service = []
    m = len(Clerk_1)
    for i in range(0,len(Arrival_NSPP)):
        U = np.random.uniform()
        k = int(U * (m-1))
        S1 = (U - ((k-1)/(m-1)))
        S2 = (m-1) * (Clerk_1[k+1] - Clerk_1[k])
        X = (S1*S2) + Clerk_1[k]
        Clerk1_Service.append(X)
        
    #Clerk 2 Service Times
    Clerk2_Service = []
    m = len(Clerk_2)
    for i in range(0,len(Arrival_NSPP)):
        U = np.random.uniform()
        k = int(U * (m-1))
        S1 = (U - ((k-1)/(m-1)))
        S2 = (m-1) * (Clerk_2[k+1] - Clerk_2[k])
        X = (S1*S2) + Clerk_2[k]
        Clerk2_Service.append(X)
    
    #Clerk 3 Service Times
    Clerk3_Service = []
    m = len(Clerk_3)
    for i in range(0,len(Arrival_NSPP)):
        U = np.random.uniform()
        k = int(U * (m-1))
        S1 = (U - ((k-1)/(m-1)))
        S2 = (m-1) * (Clerk_3[k+1] - Clerk_3[k])
        X = (S1*S2) + Clerk_3[k]
        Clerk3_Service.append(X)
    
    #########################################################################################
    
    #SIMULATION OF THE SYSTEM - BANK OF AMERICA
    Arrival_clerk1 = []
    Arrival_clerk2 = []
    Arrival_clerk3 = []
    Dep_clerk1 = []
    Dep_clerk2 = []
    Dep_clerk3 = []
    
    for i in range(0, len(Arrival_NSPP)):
        Probability = np.random.uniform()
        if Probability <= 0.60:
            Arrival_clerk1.append(Arrival_NSPP[i])
        if Probability > 0.60 and Probability <= 0.90:
            Arrival_clerk2.append(Arrival_NSPP[i])
        if Probability > 0.90 and Probability <= 1:
            Arrival_clerk3.append(Arrival_NSPP[i])
    
    if Arrival_clerk1[0] == 0:
        Dep_clerk1.append(Clerk1_Service[0])
    else:
        Dep_clerk1.append(Arrival_clerk1[0] + Clerk1_Service[0])
    
    if Arrival_clerk2[0] == 0:
        Dep_clerk2.append(Clerk2_Service[i])
    else:
        Dep_clerk2.append(Arrival_clerk2[0] + Clerk2_Service[0])
    
    if Arrival_clerk3[0] == 0:
        Dep_clerk3.append(Clerk3_Service[0])
    else:
        Dep_clerk3.append(Arrival_clerk3[0] + Clerk3_Service[0])    
    
      
    for i in range(1, len(Arrival_clerk1)):
        if Dep_clerk1[i-1] > Arrival_clerk1[i]:
            Dep_clerk1.append(Dep_clerk1[i-1] + Clerk1_Service[i])
        else:
            Dep_clerk1.append(Arrival_clerk1[i] + Clerk1_Service[i])
    
    for i in range(1, len(Arrival_clerk2)):
        if Dep_clerk2[i-1] > Arrival_clerk2[i]:
            Dep_clerk2.append(Dep_clerk2[i-1] + Clerk2_Service[i])
        else:
            Dep_clerk2.append(Arrival_clerk2[i] + Clerk2_Service[i])
    
    for i in range(1, len(Arrival_clerk3)):
        if Dep_clerk3[i-1] > Arrival_clerk3[i]:
            Dep_clerk3.append(Dep_clerk3[i-1] + Clerk3_Service[i])
        else:
            Dep_clerk3.append(Arrival_clerk3[i] + Clerk3_Service[i])
    
    ############################################################################################
    
    wait_time1 = []
    wait_time2 = []
    wait_time3 = []
    
    for i in range(0, len(Arrival_clerk1)):
        wait_time = Dep_clerk1[i] - Arrival_clerk1[i] - Clerk1_Service[i]
        wait_time1.append(wait_time)
    
    
    for i in range(0, len(Arrival_clerk2)):
        wait_time = Dep_clerk2[i] - Arrival_clerk2[i] - Clerk2_Service[i]
        wait_time2.append(wait_time)
    
    
    for i in range(0, len(Arrival_clerk3)):
        wait_time = Dep_clerk3[i] - Arrival_clerk3[i] - Clerk3_Service[i]
        wait_time3.append(wait_time)
        
    total_time3 = []
    total_time_gr15 = []
    
    for i in range(0, len(Arrival_clerk3)):
        wait_time = Dep_clerk3[i] - Arrival_clerk3[i]
        total_time3.append(wait_time)
    
    for i in range(0, len(total_time3)):
        if total_time3[i] >= 15:
            total_time_gr15.append(total_time3[i])
    
    a = np.mean(wait_time1)
    b = np.mean(wait_time2)
    c = np.mean(wait_time3)
    
    #################################

    waiting_avg.append(np.mean([a,b,c]))
    prob.append(len(total_time_gr15)/len(total_time3))
    ################################
    
print("Mean wait time",np.mean(waiting_avg))
print("Mean of Probability",np.mean(prob))
    
print("STD wait time",np.std(waiting_avg))
print("STD of Probability",np.std(prob))
    
#Confidence Intervals:
from scipy import stats
t = stats.t.ppf(1-0.025,n)
    
half_width_wait_time = t*(1.025/np.sqrt(n)) 
print(half_width_wait_time)

half_width_probability = t*(np.std(prob)/np.sqrt(n))
print(half_width_probability)





