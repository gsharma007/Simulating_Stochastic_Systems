import pandas as pd
import numpy as np
import random
import copy

np.random.seed(0)

Inter_Arrivals = [5, 8, 30, 20, 60, 80, 70, 30, 20, 90, 50]
arrival_times = [np.sum(Inter_Arrivals[:n]) for n in range(1, len(Inter_Arrivals)+1)]
setup_time = [5, 6, 8, 6, 7, 8, 7, 5, 6, 8, 7]
service_time = [180, 190, 185, 205, 170, 215, 220, 195, 200, 240, 225]
machine_av = [1, 1, 1]
operator_av = [1, 1]
depart_time = [0,0,0]
setup_depart = [0,0]
queue_level = 0
num_in_service = 0
Event_Num = 0
Event_calendar = []

service_queue = []

clock =0
pat_data = []
Test_time = 60
for x in range(0,len(arrival_times)):
    temp = {}
    temp["Pat_no"] = x
    temp["Arrival_Time"] = arrival_times[x]
    temp["service_time"] = service_time[x]
    temp["setup_time"] = setup_time[x]
    pat_data.append(temp)

# print(pat_data)
# print(arrival_times)
    
    
while(clock<10000):
    
    # print("Clock:", clock)
    val = next((item for item in pat_data if item["Arrival_Time"] == clock), False)
    # print("val:", val)
    
    # print("min_dpeart_time", min(depart_time))
    # print("min_setup_time", min(setup_depart))
    # print("len(service_queue)",len(service_queue))
    
    if(val!=False):
        
        print("Entering_1\n")
        
        if(clock >=min(depart_time) and clock >= min(setup_depart) and len(service_queue)==0):
            
            print("Clock:", clock)
            
            print("Entering_1_A\n")
            
            setup_index = setup_depart.index(min(setup_depart))
            print("setup_index:" , setup_index)
            
            depart_index = depart_time.index(min(depart_time))
            print("depart_index:" , depart_index)
            
            setup_depart[setup_index] = clock + val["setup_time"]
            print("setup_depart[setup_index]", setup_depart[setup_index])
            
            depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]
            print("depart_time[depart_index]", depart_time[depart_index])
            
            status = bool(random.getrandbits(1))
            
            print("******************************")
            print("Setup Depart Time Array: ", setup_depart)
            print("Service Depart Time Array: ",depart_time)
            print("Patient Number: ", val["Pat_no"])
            print("Test Status: ",status)
            print("*******************************")
            
            
            if(status==False):
                
                print("Adding Rework into the Arrivals")
                
                new_arrival = depart_time[depart_index] + Test_time
                
                rework_dict = {}
                
                rework_dict["Pat_no"] = val["Pat_no"]
                rework_dict["Arrival_Time"] = new_arrival
                rework_dict["service_time"] = val["service_time"]
                rework_dict["setup_time"] = val["setup_time"]
                
                #val["Arrival_Time"] = depart_time[depart_index] + Test_time
                
                print("***************")
                print("False Status")
                # print("Arrival Value:", val["Arrival_Time"])
                print("Arrival Value:", new_arrival)
                print("****************")
                
                print("rework:", rework_dict)
                
                pat_data.append(rework_dict)
                
                print("pat_data_updated:", pat_data)
                
        else:
            
            print("Clock:", clock)
            
            print("Entering 1_B\n")
            service_queue.append(val)
            
            print("service_queue:" , service_queue)
            
            
    
    if(clock>=min(depart_time) and clock >= min(setup_depart) and len(service_queue)!=0):
    
        
        print("Clock:", clock)
        print("Entering_2\n")
        
        val = service_queue.pop(0)
        print("val_now:", val)
        print("service_queue:", service_queue)
        
        setup_index = setup_depart.index(min(setup_depart))
        print("setup_index:" , setup_index)
        
        depart_index = depart_time.index(min(depart_time))
        print("depart_index:" , depart_index)
        
        setup_depart[setup_index] = clock +  val["setup_time"]
        print("setup_depart[setup_index]", setup_depart[setup_index])

        depart_time[depart_index] =  setup_depart[setup_index] + val["service_time"]
        print("depart_time[depart_index]", depart_time[depart_index])
        
        # val["setup_depart"] = setup_depart[setup_index]
        # val["depart_time"] = depart_time[depart_index]
        
        # print("changed_val:", val)
        
        status = bool(random.getrandbits(1))
        print("******************************")
        print("Setup Depart Time Array: ", setup_depart)
        print("Service Depart Time Array: ",depart_time)
        print("Patient Number: ", val["Pat_no"])
        print("Test Status: ",status)
        print("*******************************")
        
        
        if(status==False):
            
            print("Adding Rework into the Arrivals")
            
            new_arrival = depart_time[depart_index] + Test_time
                
            rework_dict = {}
            
            rework_dict["Pat_no"] = val["Pat_no"]
            rework_dict["Arrival_Time"] = new_arrival
            rework_dict["service_time"] = val["service_time"]
            rework_dict["setup_time"] = val["setup_time"]
            
            # val["Arrival_Time"] = depart_time[depart_index] + Test_time
            
            print("***************")
            print("False Status")
            # print("Arrival Value:", val["Arrival_Time"])
            print("Arrival Value:", new_arrival)
            print("****************")
            
            pat_data.append(rework_dict)
            
            print("pat_data_updated:", pat_data)

    clock+=1
    
Patient_Data = pd.DataFrame(pat_data)