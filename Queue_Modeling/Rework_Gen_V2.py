#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 01:16:56 2020
@author: gauravsharma
"""


import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

NUM_PATIENTS = 50

np.random.seed(20)


"""Testing"""

#inputs
patients_target_bc = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34 ,35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
yield_selected_mfg = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]


def high_fidelity_test_case_A():
    
    P_1_HF = 0.99   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_HF = 0.10   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_HF = 0.65   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    #calculating P(Y'>= Y* / Ytilda>= Y*) 
    #i.e. proability of measured yield being more than expected yield given calculated yield is more than expected
    #P(Y'>= Y* / Ytilda>= Y*)  = P(Ytilda >= Y* / Y' >= Y*) * P(Y' >= Y*) / [P(Ytilda >= Y* / Y' >= Y*) * P(Y' >= Y*) + P(Ytilda >= Y* / Y' < Y*) * P(Y' < Y*)]
    alpha_HF = (P_1_HF * P_3_HF) / (P_1_HF * P_3_HF + P_2_HF * (1 - P_3_HF))

    U1 = np.random.uniform(0, 1)

    if (U1 <= alpha_HF):
        Test_Result = "Sample Passed"
    else:
        Test_Result = "Sample Rejected"
    return Test_Result
        
def high_fidelity_test_case_B():
    
    P_1_HF = 0.99   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_HF = 0.10   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_HF = 0.65   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    Beta_HF = ((1-P_1_HF)* P_3_HF) / (((1-P_1_HF)* P_3_HF) + ((1-P_2_HF)*(1-P_3_HF)))

    U2 = np.random.uniform(0, 1)

    if (U2 <= Beta_HF):
        Test_Result = "Sample Passed"    #It was fail, and Test confirms Pass
    else:
        Test_Result = "Sample Rejected"  #It was fail, Test Confirms Fail
    return Test_Result

def low_fidelity_test_case_A():
    
    P_1_LF = 0.85   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_LF = 0.45   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_LF = 0.40   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    #calculating P(Y'>= Y* / Ytilda < Y*)

    alpha_LF = (P_1_LF * P_3_LF) / (P_1_LF * P_3_LF + P_2_LF * (1 - P_3_LF))

    U3 = np.random.uniform(0, 1)

    if (U3 <= alpha_LF):
        Test_Result = "Sample Passed"
    else:
        Test_Result = "Sample Rejected"
    return Test_Result

def low_fidelity_test_case_B():
    
    P_1_LF = 0.85   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
    P_2_LF = 0.45   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
    P_3_LF = 0.40   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

    Beta_LF = ((1-P_1_LF)* P_3_LF) / (((1-P_1_LF)* P_3_LF) + ((1-P_2_LF)*(1-P_3_LF)))

    U4 = np.random.uniform(0, 1)

    if (U4 <= Beta_LF):
        Test_Result = "Sample Passed"    #It was fail, but Test confirms Pass
    else:
        Test_Result = "Sample Rejected"  #It was fail, Test Confirms Fail    
    return Test_Result

def quality_policy(QM_Policy_MFG, yield_selected_mfg,patients_target_bc, val):
    
    a = val["Pat_no"]
    
    print("index_qm:", a)

    #defining level for each quality control policy
    #Test happens according to that level and the results are recorded
    Test_Result=""

    if QM_Policy_MFG == 1:

        #test everything in high fidelity

        #Case A
        if (yield_selected_mfg[a] > patients_target_bc[a]):
            Test_Result=high_fidelity_test_case_A()
        #Case B
        else:
            Test_Result=high_fidelity_test_case_B()


    elif QM_Policy_MFG == 2:

        #test everything in low fidelity and if test fails then check again in high fidelity

        #Case A
        if (yield_selected_mfg[a] > patients_target_bc[a]):
            Test_Result = low_fidelity_test_case_A()
            
            if Test_Result == "Sample Rejected":
                Test_Result = high_fidelity_test_case_A()
                if Test_Result == "Sample Rejected":
                    Test_Result = "Rejected in LF and HF Both"
                else:
                    Test_Result = "Rejected in LF but Passed in HF"

        #Case B
        else:
            Test_Result= low_fidelity_test_case_B()

            if Test_Result == "Sample Rejected":
                Test_Result = high_fidelity_test_case_B()
                if Test_Result == "Sample Rejected":
                    Test_Result = "Rejected in LF and HF Both"
                else:
                    Test_Result = "Rejected in LF, Passed in HF"
                    
    else:

        U5 = np.random.uniform(0, 1)

        if (U5 <= 0.70):

            if (yield_selected_mfg[a] > patients_target_bc[a]):
                Test_Result=high_fidelity_test_case_A()
            else:
                Test_Result=high_fidelity_test_case_B()

        else:
            Test_Result= "Proceeding Sample without contamination"

    return Test_Result

"""Resource allocation and Rework"""

Inter_Arrivals = np.random.uniform(20, 50, size=NUM_PATIENTS)

# arrival_times = [10, 10]

arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]
arrival_times = np.around(arrival_times)
arrival_times[7]=arrival_times[6]

service_time = np.random.uniform(192,240, size=NUM_PATIENTS)
service_time = np.around(service_time)

setup_time = np.random.uniform(17, 26,size=NUM_PATIENTS)
setup_time = np.around(setup_time)

#Resource Count

Num_Operators = 3
Num_Machines = 5

#Initialization
clock =0
setup_depart = [0]*Num_Operators
depart_time = [0]*Num_Machines
Event_Num = 0
Event_calendar = []
departures = []
service_queue = []
Queue_track = []
results = []
rework_df = []
rework_check = []

queue_level = 0
num_in_service = 0
num_in_system = 0
num_completed = 0
num_in_rework = 0
#num_remaining = 50
min_nonzero = 0
B_t = []


pat_data = []
Test_time = 2
for x in range(0,len(arrival_times)):
    temp = {}
    temp["Pat_no"] = x
    temp["Arrival_Time"] = arrival_times[x]
    temp["service_time"] = service_time[x]
    temp["setup_time"] = setup_time[x]
    temp["is_rework"] = "No"
    pat_data.append(temp)


def Average(lst): 
    return sum(lst) / len(lst)

while(clock<10000):
    no_val = 0
    #print("Clock:", clock)
    val = next((item for item in pat_data if item["Arrival_Time"] == clock), False)
    for x  in pat_data:
        if x["Arrival_Time"]==clock:
            no_val += 1

    while(no_val>0):   
         
        depart_non_zero_count = np.count_nonzero(depart_time)
        if depart_non_zero_count != 0:
            min_nonzero = min([num for num in depart_time if num !=0])
            
        """Case_1"""    
        
        if(clock!=0 and clock == min_nonzero and len(service_queue)==0):
            
            print("Clock:", clock)
            print("Entering_1\n")
            
            num_in_system -= 1
            num_in_service -= 1
            num_completed += 1
            
            depart_index = depart_time.index(clock)
            depart_time[depart_index] = 0
            
            print("depart_time[depart_index]", depart_time[depart_index])
            
            """Operator state tracking"""
            #busy- 1 and idle- 0
            operator_state = []
            
            for op in setup_depart:
                if op > clock:
                    state = 1
                    operator_state.append(state)
                else:
                    state = 0
                    operator_state.append(state)
                    
            print("operator_state:", operator_state)
            
            OP_state = Average(operator_state)
            
            OP_bt = (np.count_nonzero(operator_state)/len(operator_state))*100
            
            
            
            """Machine state tracking"""
            #busy- 1 and idle- 0
            machine_state = []
            
            for mc in depart_time:
                if mc > 0:
                    state = 1
                    machine_state.append(state)
                else:
                    state = 0
                    machine_state.append(state)
                    
            print("machine_state:", machine_state)
            
            MC_state = Average(machine_state)
            
            MC_bt = (np.count_nonzero(machine_state)/len(machine_state))*100
            
            
            print("******************************")
            print("Setup Depart Time Array: ", setup_depart)
            print("Service Depart Time Array: ",depart_time)
            #print("Patient Number: ", val["Pat_no"])
            print("*******************************")
            
            Event_info = {#"Patient": val["Pat_no"], 
                  "Event_time" : clock, 
                  "Event_Type" : "Departure",
                  "Num_in_System" : num_in_system,
                  "Num_in_Queue" : queue_level,
                  "Num_in_Service" : num_in_service,
                  "Num_Completed" : num_completed,
                  "Num_in_Rework" : num_in_rework,
                  #"Calling_Population" : Calling_Population,
                  "Operator_State" : operator_state,
                  "OP_state" : OP_state,
                  "OP_B(t)" : OP_bt,
                  "Machine_State" : machine_state,
                  "MC_state" : MC_state,
                  "MC_B(t)" : MC_bt} 
            
            print("Event_info:\n", Event_info)
            
            Event_calendar.append(Event_info)
            results.append(Event_info)
    
        """Case_2"""
        
        if(val!=False):
            
            print("Entering_2\n")
            
            if(clock >=min(depart_time) and clock >= min(setup_depart) and len(service_queue)==0):
                
                print("Clock:", clock)
                
                print("Entering_2_A\n")
                
                setup_index = setup_depart.index(min(setup_depart))
                depart_index = depart_time.index(min(depart_time))
                setup_depart[setup_index] = clock + val["setup_time"]           
                depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]

                """Operator state tracking"""
                #busy- 1 and idle- 0
                operator_state = []
                
                for op in setup_depart:
                    if op > clock:
                        state = 1
                        operator_state.append(state)
                    else:
                        state = 0
                        operator_state.append(state)
                        
                OP_state = Average(operator_state)

                OP_bt = (np.count_nonzero(operator_state)/len(operator_state))*100
                
                """Machine state tracking"""
                #busy- 1 and idle- 0
                machine_state = []
                
                for mc in depart_time:
                    if mc > clock:
                        state = 1
                        machine_state.append(state)
                    else:
                        state = 0
                        machine_state.append(state)

                MC_state = Average(machine_state) 
                MC_bt = (np.count_nonzero(machine_state)/len(machine_state))*100
                    
                #else:
                num_in_service += 1
                num_in_system += 1
                
                if val["is_rework"] in ("Yes"):
                    num_in_rework += 1
                
                #status = bool(random.getrandbits(1))
                Test_Result = quality_policy(1, yield_selected_mfg, patients_target_bc, val)
                
                print("******************************")
                print("Setup Depart Time Array: ", setup_depart)
                print("Service Depart Time Array: ",depart_time)
                print("Patient Number: ", val["Pat_no"])
                print("Test Status: ",Test_Result)
                print("*******************************")

                if Test_Result in ("Sample Rejected","Rejected in LF and HF Both"):
                    
                    print("Adding Rework into the Arrivals")
                    new_arrival = depart_time[depart_index] + Test_time
                    rework_dict = {}
                    rework_dict["Pat_no"] = val["Pat_no"]
                    rework_dict["Arrival_Time"] = new_arrival
                    rework_dict["service_time"] = val["service_time"]
                    rework_dict["setup_time"] = val["setup_time"]
                    rework_dict["is_rework"] = "Yes"
                    rework_df.append(rework_dict)
                    
                    #val["Arrival_Time"] = depart_time[depart_index] + Test_time
                    
                    print("***************")
                    print("False Status")
                    # print("Arrival Value:", val["Arrival_Time"])
                    print("Arrival Value:", new_arrival)
                    print("****************")
                    
                    pat_data.append(rework_dict)

                Event_info = {"Patient": val["Pat_no"], 
                              "Arrival_time": val["Arrival_Time"],
                              "Event_time" : clock, 
                              "Event_Type" : "Arrival and Service Start",
                              "Waiting_time" : (clock-val["Arrival_Time"]),
                              "Num_in_System" : num_in_system,
                              "Num_in_Queue" : queue_level,
                              "Num_in_Service" : num_in_service,
                              "Num_Completed" : num_completed,
                              "Num_in_Rework" : num_in_rework,
                              "Calling_Population" : (NUM_PATIENTS - num_in_system - num_completed),
                              "Operator": "O"+str(setup_index),
                              "Operator_State" : operator_state,
                              "OP_state" : OP_state,
                              "OP_B(t)" : OP_bt, 
                              "Setup_time" : val["setup_time"],
                              "Setup_finish" : setup_depart[setup_index],
                              "Bioreactor": "M"+str(depart_index),
                              "Machine_State" : machine_state,
                              "MC_state" : MC_state,
                              "MC_B(t)" : MC_bt,
                              "Service_time": val["service_time"],
                              "Departure" : depart_time[depart_index],
                              "Test_Reseult": Test_Result}
                
                print("Event_info:\n", Event_info)
                Event_calendar.append(Event_info)
                results.append(Event_info)
                Queue_track.append(queue_level)
           
            else:
                
                print("Clock:", clock)
                
                print("Entering 2_B\n")
                service_queue.append(val)
                
                num_in_system += 1
                queue_level = len(service_queue)
                Queue_track.append(queue_level)
                
                if val["is_rework"] in ("Yes"):
                    num_in_rework += 1
                
                Event_info = {"Patient": val["Pat_no"], 
                              "Arrival_time": val["Arrival_Time"],
                              "Event_time" : clock, 
                              "Event_Type" : "Arrival and in Queue",
                              "Waiting_time" : (clock-val["Arrival_Time"]),
                              "Num_in_System" : num_in_system,
                              "Num_in_Queue" : queue_level,
                              "Num_in_Service" : num_in_service,
                              "Num_Completed" : num_completed,
                              "Num_in_Rework" : num_in_rework,
                              "Calling_Population" : (NUM_PATIENTS - num_in_system - num_completed),
                              "Operator_State" : operator_state,
                              "OP_state" : OP_state,
                              "OP_B(t)" : OP_bt,
                              "Machine_State" : machine_state,
                              "MC_state" : MC_state,
                              "MC_B(t)" : MC_bt} 
                
                print("Event_info:\n", Event_info)    
                Event_calendar.append(Event_info)

        """Case_3"""
        
        if(clock>=min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
 
            print("Clock:", clock)
            print("Entering_3\n")
            
            val = service_queue.pop(0)
            queue_level = len(service_queue)
            Queue_track.append(queue_level)
            setup_index = setup_depart.index(min(setup_depart))
            depart_index = depart_time.index(min(depart_time))
            setup_depart[setup_index] = clock +  val["setup_time"]
            depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]
           
            """Operator state tracking"""
            #busy- 1 and idle- 0
            operator_state = []
            
            for op in setup_depart:
                if op > clock:
                    state = 1
                    operator_state.append(state)
                else:
                    state = 0
                    operator_state.append(state)
                    
            OP_state = Average(operator_state)
            
            OP_bt = (np.count_nonzero(operator_state)/len(operator_state))*100
            
            """Machine state tracking"""
            #busy- 1 and idle- 0
            machine_state = []
            
            for mc in depart_time:
                if mc > 0:
                    state = 1
                    machine_state.append(state)
                else:
                    state = 0
                    machine_state.append(state)

            MC_state = Average(machine_state)

            MC_bt = (np.count_nonzero(machine_state)/len(machine_state))*100
    
            num_in_system -= 1
            num_completed += 1
            
            Test_Result = quality_policy(1, yield_selected_mfg, patients_target_bc, val)
            
            print("******************************")
            print("Setup Depart Time Array: ", setup_depart)
            print("Service Depart Time Array: ",depart_time)
            print("Patient Number: ", val["Pat_no"])
            print("Test Status: ",Test_Result)
            print("*******************************")

            if Test_Result in ("Sample Rejected","Rejected in LF and HF Both"):
                
                print("Adding Rework into the Arrivals")
                
                num_completed -= 1
                
                new_arrival = depart_time[depart_index] + Test_time
                    
                rework_dict = {}
                
                rework_dict["Pat_no"] = val["Pat_no"]
                rework_dict["Arrival_Time"] = new_arrival
                rework_dict["service_time"] = val["service_time"]
                rework_dict["setup_time"] = val["setup_time"]
                rework_dict["is_rework"] = "Yes"
                
                rework_df.append(rework_dict)

                print("***************")
                print("False Status")
                # print("Arrival Value:", val["Arrival_Time"])
                print("Arrival Value:", new_arrival)
                print("****************")
                
                pat_data.append(rework_dict)
            
            Event_info = {"Patient": val["Pat_no"], "Arrival_time": val["Arrival_Time"],
                          "Event_time" : clock, "Event_Type" : "Departure and Service_Start",
                          "Waiting_time" : (clock-val["Arrival_Time"]),
                          "Num_in_System" : num_in_system,
                          "Num_in_Queue" : queue_level,
                          "Num_in_Service" : num_in_service,
                          "Num_Completed" : num_completed,
                          "Num_in_Rework" : num_in_rework,
                          "Calling_Population" : (NUM_PATIENTS - num_in_system - num_completed),
                          "Operator": "O"+str(setup_index),
                          "Operator_State" : operator_state,
                          "OP_state" : OP_state,
                          "OP_B(t)" : OP_bt,
                          "Setup_time" : val["setup_time"],
                          "Setup_finish" : setup_depart[setup_index],
                          "Bioreactor": "M"+str(depart_index),
                          "Machine_State" : machine_state,
                          "MC_state" : MC_state,
                          "MC_B(t)" : MC_bt,
                          "Service_time": val["service_time"],
                          "Departure" : depart_time[depart_index], 
                          "Test_Reseult": Test_Result}
            
            print("Event_info:\n", Event_info)
            
            Event_calendar.append(Event_info)
            results.append(Event_info)
        no_val -=1
    clock+=1
    

"""Storing Results"""

Event_calendar = pd.DataFrame(Event_calendar)
Event_calendar['queue'] = Queue_track


Patient_Data = pd.DataFrame(pat_data)

df = pd.DataFrame(results)

"""System Visualization"""

plt.figure()
Event_calendar.plot(x='Event_time', y=['queue','Calling_Population', 'Num_in_Rework', 'Num_in_Service', 'Num_Completed'], 
                     kind='area', stacked=True, label = ['parts_in_queue','calling_population', 'parts_in_rework', 'parts_in_service', 'parts_completed'],
                     grid=True)
plt.show()

plt.figure()
Event_calendar.plot(x='Event_time', y=['queue', 'Calling_Population', 'Num_in_Rework', 'Num_Completed'], 
                     kind='area', stacked=True, 
                     grid=True)
plt.show()

plt.figure()
Event_calendar.plot(x='Event_time', y=['queue', 'Calling_Population', 'Num_in_Rework'], 
                     kind='area', stacked=True, 
                     grid=True)
plt.show()


plt.figure()
Event_calendar.plot(x='Event_time', y='queue', linestyle='-', drawstyle='steps')
plt.show()

plt.figure()
waiting_time_dist = Event_calendar.plot(x='Event_time', y='Waiting_time', 
                                kind= 'area', subplots = True)
plt.show()


plt.figure()
num_in_sys_dist = Event_calendar.plot(x='Event_time', y='Num_in_System')
plt.show()

plt.figure()
Event_calendar.plot(x='Event_time', y='OP_B(t)', kind='line', linestyle='-', label = 'OP_B(t)')
plt.show()

plt.figure()
Event_calendar.plot(x='Event_time', y='MC_B(t)', kind='line', linestyle='-', label = 'MC_B(t)')
plt.show()

"""System Statistics"""

average_queue_level = sum(Queue_track)/len(Queue_track)
print("average_queue_level :", average_queue_level)

average_people_in_system = sum(Event_calendar['Num_in_System'])/len(Queue_track)
print("average_people_in_system :", average_people_in_system)

Time_average_number_in_queue = sum(Queue_track)/max(depart_time)
print("Time_average_number_in_queue", Time_average_number_in_queue)

avg_wait_time_in_queue = sum(Event_calendar['Waiting_time'])/np.count_nonzero(Queue_track)
print("avg_wait_time_in_queue", avg_wait_time_in_queue)

operator_utilization = (sum(Event_calendar['OP_B(t)'])/(Num_Operators*max(depart_time)))*100
print("operator_utilization", operator_utilization)

machine_tilization = (sum(Event_calendar['MC_B(t)'])/(Num_Machines*max(depart_time)))*100
print("machine_tilization", machine_tilization)
