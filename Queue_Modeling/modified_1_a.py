import pandas as pd
import numpy as np
import bisect

NUM_PATIENTS = 10

np.random.seed(0)

# Inter_Arrivals = [5, 8, 30, 20, 60, 80, 70, 30, 20, 90, 50]
# arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]

setup_time = [25, 26, 28, 26, 27, 28, 27, 15, 16, 18, 17]
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
    index = arrival_times.index(clock)
    if(clock >=min(depart_time) and clock >= min(setup_depart)  and len(service_queue)==0):
        setup_index = setup_depart.index(min(setup_depart))
        depart_index = depart_time.index(min(depart_time))
        setup_depart[setup_index] = clock + setup_time[index]
        depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
        Event_info = {"Patient": "P"+str(index), "Event_time" : clock, 
                      "Event_Type" : "Arrival and Service Start", 
                      "Setup_finish" : setup_depart[setup_index],
                      "Departure" : depart_time[depart_index]}
        Event_calendar.append(Event_info)
    else:
        service_queue.append(index)
        queue_level = len(service_queue)
        Event_info = {"Patient": "P"+str(index), "Event_time" : clock, 
                      "Event_Type" : "Arrival and in Queue"}

def handle_departure_event():
    index = service_queue.pop(0)
    setup_index = setup_depart.index(min(setup_depart))
    depart_index = depart_time.index(min(depart_time))
    setup_depart[setup_index] = clock + setup_time[index]
    depart_time[depart_index] =  setup_depart[setup_index] + service_time[index]
    Event_info = {"Patient": "P"+str(index), "Event_time" : clock, 
                  "Event_Type" : "Service_Start", "Setup_finish" : setup_depart[setup_index],
                  "Departure" : depart_time[depart_index]}
    Event_calendar.append(Event_info)    

clock =0

while(clock<1000):   
    
    if(clock in arrival_times):
        handle_arrival_event()
    if(clock>=min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
        handle_departure_event()
        
    clock+=1
    
print("Full_Event_Calendar:\n" , Event_calendar)

pd["Arrival_times"] = arrival_times
pd = pd.DataFrame(Event_calendar)
