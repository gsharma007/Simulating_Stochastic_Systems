import pandas as pd
import numpy as np

NUM_PATIENTS = 10

np.random.seed(0)

# Inter_Arrivals = [5, 8, 30, 20, 60, 80, 70, 30, 20, 90, 50]
# arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]

setup_time = [25, 26, 20, 26, 27, 28, 27, 15, 16, 18, 17]
# len(setup_time)

Inter_Arrivals = np.random.randint(20, 50, size=NUM_PATIENTS)
arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]

service_time = np.random.randint(192,240, size=NUM_PATIENTS)


# service_time = [180, 190, 185, 205, 170, 215, 220, 195, 200, 240, 225]
# len(service_time)

#Resource Count

Num_Operators = 1
Num_Machines = 4

#Initialization

clock = 0
setup_depart = [0]*Num_Operators
depart_time = [0]*Num_Machines
queue_level = 0
Event_Num = 0
Event_calendar = []
departures = []
service_queue = []

def handle_arrival_event():
    
    # print("min_depart_time:", min(depart_time))
    # print("min_setup_depart:", min(setup_depart))
    # print("Entering_1")
    print("clock_now:", clock)
    
    index = arrival_times.index(clock)
    #print("index_value:", index)
    
    if(clock >=min(depart_time) and clock >= min(setup_depart)  and len(service_queue)==0):
        
        #setup_time = np.random.randint(25,38)
        #setup_times.append(setup_time)
        
        print("Entering_1A")
        setup_index = setup_depart.index(min(setup_depart))
        print("setup_index:", setup_index)
        depart_index = depart_time.index(min(depart_time))
        print("depart_index:",depart_index)
        setup_depart[setup_index] = clock + setup_time[index]
        depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
        print("This is setup_depart time:",setup_depart)
        print("This is depart Time:",depart_time)
        
        #departures.append(depart_time)
        
    else:
        print("Entering_1B")
        service_queue.append(index)
        print("Service_Queue:", service_queue)
        queue_level = len(service_queue)
        print("queue_level:", queue_level)

def handle_departure_event():
    
    #setup_time = np.random.randint(25, 38)
    #setup_times.append(setup_time)
    
    print("clock_now:", clock)
    
    # print("min_depart_time:", min(depart_time))
    # print("min_setup_depart:", min(setup_depart))
    
    print("Entering_2")
    index = service_queue.pop(0)
    print("service_queue:", service_queue)
    print("index:", index)
    setup_index = setup_depart.index(min(setup_depart))
    print("setup_index:", setup_index)
    depart_index = depart_time.index(min(depart_time))
    print("depart_index:",depart_index)
    setup_depart[setup_index] = clock + setup_time[index]
    depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
    print("This is setup_depart time:",setup_depart)
    print("This is depart Time:",depart_time)
    
    #departures.append(depart_time)
    

clock =0
setup_times = []

# print(arrival_times)
while(clock<1000):
    #print("clock:", clock)   
    
    if(clock in arrival_times):
        
        handle_arrival_event()
        
    if(clock>=min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
         
        handle_departure_event()
        
        
    clock+=1