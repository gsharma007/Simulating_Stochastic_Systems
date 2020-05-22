import pandas as pd
import numpy as np

Inter_Arrivals = [5, 8, 30, 20, 60, 80, 70, 30, 20, 90, 50]
arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]

setup_time = [5, 6, 8, 6, 7, 8, 7, 5, 6, 8, 7]
len(setup_time)

service_time = [180, 190, 185, 205, 170, 215, 220, 195, 200, 240, 225]
len(service_time)

machine_av = [1, 1, 1]
operator_av = [1, 1]
clock = 0
depart_time = [0,0,0]
setup_depart = [0,0]
queue_level = 0
num_in_service = 0
Event_Num = 0
Event_calendar = []

service_queue = []

def handle_arrival_event():
    
    # print("min_depart_time:", min(depart_time))
    # print("min_setup_depart:", min(setup_depart))
    # print("Entering_1")
    # print("clock_now:", clock)
    
    index = arrival_times.index(clock)
    #print("index_value:", index)
    
    if(clock >=min(depart_time) and clock >= min(setup_depart)):
        
        print("Entering_1A")
        setup_index = setup_depart.index(min(setup_depart))
        print("setup_index:", setup_index)
        depart_index = depart_time.index(min(depart_time))
        print("depart_index:",depart_index)
        setup_depart[setup_index] = clock + setup_time[index]
        depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
        print("This is depart Time:",depart_time)
        print("This is setup_depart time:",setup_depart)
    else:
        print("Entering_1B")
        service_queue.append(index)
        print("Service_Queue:", service_queue)
        queue_level = len(service_queue)
        print("queue_level:", queue_level)

def handle_departure_event():
    
    # print("min_depart_time:", min(depart_time))
    # print("min_setup_depart:", min(setup_depart))
    
    print("Entering_2")
    index = service_queue.pop()
    print("service_queue:", service_queue)
    print("index:", index)
    setup_index = setup_depart.index(min(setup_depart))
    print("setup_index:", setup_index)
    depart_index = depart_time.index(min(depart_time))
    print("depart_index:",depart_index)
    setup_depart[setup_index] = clock + setup_time[index]
    depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
    print("This is depart Time:",depart_time)
    print("This is setup_depart time:",setup_depart)



clock =0
# print(arrival_times)
while(clock<1000):
    #print("clock:", clock)   
    
    if(clock in arrival_times):
        
        handle_arrival_event()
        
    if(clock==min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
        
        handle_departure_event()
        
        
    clock+=1