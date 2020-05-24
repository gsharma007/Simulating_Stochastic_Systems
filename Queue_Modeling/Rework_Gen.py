#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:16:56 2020

@author: gauravsharma
"""


import pandas as pd
import numpy as np
import random
#import bisect
import matplotlib.pyplot as plt

NUM_PATIENTS = 10

np.random.seed(0)

Inter_Arrivals = np.random.uniform(20, 50, size=NUM_PATIENTS)

arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]
arrival_times = np.around(arrival_times)

service_time = np.random.uniform(192,240, size=NUM_PATIENTS)
service_time = np.around(service_time)

setup_time = np.random.uniform(17, 26,size=NUM_PATIENTS)
setup_time = np.around(setup_time)

#Resource Count

Num_Operators = 2
Num_Machines = 3

#Initialization
clock =0
setup_depart = [0]*Num_Operators
depart_time = [0]*Num_Machines
queue_level = 0
Event_Num = 0
Event_calendar = []
departures = []
service_queue = []
Queue_track = []
results = []
num_in_service = 0
B_t = []


pat_data = []
Test_time = 2
for x in range(0,len(arrival_times)):
    temp = {}
    temp["Pat_no"] = x
    temp["Arrival_Time"] = arrival_times[x]
    temp["service_time"] = service_time[x]
    temp["setup_time"] = setup_time[x]
    pat_data.append(temp)


while(clock<10000):

    val = next((item for item in pat_data if item["Arrival_Time"] == clock), False)
    
    if(val!=False):
        
        if(clock >=min(depart_time) and clock >= min(setup_depart) and len(service_queue)==0):
            setup_index = setup_depart.index(min(setup_depart))
            depart_index = depart_time.index(min(depart_time))
            setup_depart[setup_index] = clock + val["setup_time"]
            depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]
            status = bool(random.getrandbits(1))
            
            print("******************************")
            print("Setup Depart Time Array: ", setup_depart)
            print("Service Depart Time Array: ",depart_time)
            print("Patient Number: ", val["Pat_no"])
            print("Test Status: ",status)
            print("*******************************")
            
            Event_info = {"Patient": val["Pat_no"], 
                          "Arrival_time": val["Arrival_Time"],
                          "Event_time" : clock, 
                          "Event_Type" : "Arrival and Service Start", 
                          "Operator": "O"+str(setup_index),
                          "Setup_time" : val["setup_time"],
                          "Bioreactor": "M"+str(depart_index),
                          "Service_time": val["service_time"],
                          "Setup_finish" : setup_depart[setup_index],
                          "Departure" : depart_time[depart_index], "Test_Reseult": status}
            
            Event_calendar.append(Event_info)
            results.append(Event_info)
            
            Queue_track.append(queue_level)
            
            if(status==False):
                
                print("Adding Rework into the Arrivals")
                new_arrival = depart_time[depart_index] + Test_time
                rework_dict = {}
                
                rework_dict["Pat_no"] = val["Pat_no"]
                rework_dict["Arrival_Time"] = new_arrival
                rework_dict["service_time"] = val["service_time"]
                rework_dict["setup_time"] = val["setup_time"]
                
                print("***************")
                print("False Status")
                # print("Arrival Value:", val["Arrival_Time"])
                print("Arrival Value:", new_arrival)
                print("****************")

                pat_data.append(rework_dict)
                
        else:

            service_queue.append(val)
            
            Event_info = {"Patient": val["Pat_no"], 
                          "Arrival_time": val["Arrival_Time"],
                          "Event_time" : clock, 
                          "Event_Type" : "Arrival and in Queue"}

            Event_calendar.append(Event_info)
            
            queue_level = len(service_queue)
            Queue_track.append(queue_level)

    if(clock>=min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
        
        val = service_queue.pop(0)
        
        queue_level = len(service_queue)
        Queue_track.append(queue_level)
        
        setup_index = setup_depart.index(min(setup_depart))
        depart_index = depart_time.index(min(depart_time))
        setup_depart[setup_index] = clock +  val["setup_time"]
        depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]
        
        status = bool(random.getrandbits(1))
        print("******************************")
        print("Setup Depart Time Array: ", setup_depart)
        print("Service Depart Time Array: ",depart_time)
        print("Patient Number: ", val["Pat_no"])
        print("Test Status: ",status)
        print("*******************************")
        
        
        Event_info = {"Patient": val["Pat_no"], "Arrival_time": val["Arrival_Time"],
                      "Event_time" : clock, "Event_Type" : "Service_Start", 
                      "Operator": "O"+str(setup_index),
                      "Setup_time" : val["setup_time"],
                      "Bioreactor": "M"+str(depart_index),
                      "Service_time": val["service_time"],
                      "Setup_finish" : setup_depart[setup_index],
                      "Departure" : depart_time[depart_index], "Test_Reseult": status}
        
        Event_calendar.append(Event_info)
        results.append(Event_info)
        
        if(status==False):
            
            print("Adding Rework into the Arrivals")
            
            new_arrival = depart_time[depart_index] + Test_time
            rework_dict = {}
            
            rework_dict["Pat_no"] = val["Pat_no"]
            rework_dict["Arrival_Time"] = new_arrival
            rework_dict["service_time"] = val["service_time"]
            rework_dict["setup_time"] = val["setup_time"]
            
            print("***************")
            print("False Status")
            # print("Arrival Value:", val["Arrival_Time"])
            print("Arrival Value:", new_arrival)
            print("****************")
            
            pat_data.append(rework_dict)

    clock+=1
    

"""Storing Results"""

print("Full_Event_Calendar:\n" , Event_calendar)
Event_calendar = pd.DataFrame(Event_calendar)
Event_calendar['queue'] = Queue_track
#Event_calendar["B(t)"] = B_t

Patient_Data = pd.DataFrame(pat_data)

df = pd.DataFrame(results)
df["waiting_time"]= df["Event_time"]-df["Arrival_time"]

"""System Visualization"""

plt.figure()
queue_graph = Event_calendar.plot(x='Event_time', y='queue', drawstyle="steps")
plt.show()

"""System Statistics"""

#Average Queue Level = sum(Queue_Level)/No. of times in queue
average_queue_level = sum(Queue_track)/len(Queue_track)
print("average_queue_level :", average_queue_level)

#Average waiting time in queue = Total of times in queue/No. of times in queue
avg_wait_time_in_queue = sum(df['waiting_time'])/np.count_nonzero(Queue_track)
print("avg_wait_time_in_queue", avg_wait_time_in_queue)
