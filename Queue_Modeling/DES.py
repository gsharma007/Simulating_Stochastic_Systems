#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 21:01:25 2020

@author: gauravsharma
"""

import numpy as np
import pandas as pd
import seaborn as sns

df = pd.DataFrame()

class Simulation:
    def __init__(self):
        self.num_in_system = 0
        self.clock = 0.0
        self.t_arrival = self.generate_interarrival()
        self.t_depart = float('inf') 
        self.num_arrivals = 0
        self.num_departs = 0
        self.total_wait = 0.0
        self.tmp_time = self.generate_service()
        
    def advance_time(self):
        t_event = min(self.t_arrival, self.t_depart)
        self.total_wait += self.num_in_system*(t_event - self.clock)
        self.clock = t_event
        if self.t_arrival <= self.t_depart:
            self.handle_arrival_event()
        else:
            self.handle_depart_event()
    
    def handle_arrival_event(self):
        self.num_in_system += 1
        self.num_arrivals += 1
        if self.num_in_system <= 1:
            self.temp1 = self.generate_service()
            print(">>>>>>>>",self.temp1)
            self.tmp_time=self.temp1
            self.t_depart = self.clock + self.temp1
        self.t_arrival = self.clock + self.generate_interarrival()
        
    def handle_depart_event(self):
        self.num_in_system -= 1
        self.num_departs += 1
        if self.num_in_system > 0:
            self.temp2=self.generate_service();
            print(">>>>><<<<<",self.temp2)
            self.tmp_time = self.temp2
            self.t_depart = self.clock + self.temp2
        else:
            self.t_depart = float("inf")
    
    def generate_interarrival(self):
        return np.random.lognormal(mean=0.6, sigma=0.3)
    def generate_service(self):
        return np.random.uniform(low = 5, high = 8)

np.random.seed(0)
  
s = Simulation()


clock_time = []
arrival_times = []
service_times = []
departures = []
event_calendar = []

for i in range(200):
    s.advance_time()
    a = s.clock
    b = s.t_arrival
    c = s.tmp_time
    d = s.t_depart
    clock_time.append(a)
    arrival_times.append(b)
    service_times.append(c)
    departures.append(d)
    
    event_list = {"Iteration": "I_"+str(i), "Event_time": a,
                  "Arrival_time": b, "Service_time": c, "Departure_time": d}
    event_calendar.append(event_list)
    print(event_calendar)
    
df["clock_time"] = clock_time
df["arrival_times"] = arrival_times
df["service_times"] = service_times
df["departures"] =  departures

import matplotlib.pyplot as plt

# =============================================================================
# plt.figure()
# sns.lineplot(df.index, df['arrival_times'], drawstyle='steps-pre')
# #df.plot(x='arrival_times', drawstyle="steps", linewidth=2)
# plt.show()
# =============================================================================