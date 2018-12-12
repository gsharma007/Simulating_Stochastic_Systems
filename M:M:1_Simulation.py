#M/M/1 Queue Simulation
#By Gaurav Sharma

from statistics import mean

#transformation of interarrival data1 and servicetime data2
import matplotlib.pyplot as plot  # plotting the statistics
import numpy as np
import simpy as sp #calculating the statistics

#step-1importing data
data1 =f = open('Data1.txt', 'r')
data2 = f = open('Data2.txt', 'r')

lambda1 = (0.9)**-1; #arrival rate
mu = (0.7)**-1; #service rate

def generate_interarrivaltime():
    return np.random.exponential((lambda1)**-1) #step2a-transformation to exponential

def generate_servicetime():
    return np.random.exponential((mu)**-1) #step2b-transformation to exponential

def queue_run(env,servers):
    i=0
    while True:
        i+=1
        yield env.timeout(generate_interarrivaltime())
        env.process(customer(env,i,servers))

waiting_time = []

def customer(env,customer,servers):
    with servers.request() as request:
        t_arrival = env.now
        print (env.now, 'customer {} arrives'.format(customer))
        print (env.now, 'customer {} departs'.format(customer))
        t_depart = env.now
        waiting_time.append(t_depart - t_arrival)

obs_times = []
q_length = []

def observe(env,servers):
    while True:
        obs_times.append(env.now)
        q_length.append(len(servers.queue))
        yield env.timeout(0.5)

np.random.seed(0)

env = sp.Environment()

servers = sp.Resource(env, capacity=1)

env.process(queue_run(env, servers))
env.process(observe(env, servers))

env.run(until=1000)

no_of_elements = len(q_length)
sum_of_elements = sum(q_length)

def Average(q_length):
    return sum(q_length)/len(q_length)

#task3-Showing statistics
average = Average (q_length)
print("Average number of entities in queue throughout the simulation is:", round(average,4))

a1 = np.array([])
a2 = a1[a1>2]

print(a1)
print (a2)

print(len(a2))
percentage = len(a2)/len(a1)*100
print(percentage, 'percentage of time when there are 3 or more entities in the queue is')

rho= (lambda1/mu)*100 #offered load i.e. server utilization
print(rho, 'Total percentage server utilization is')

#plotting the graphs
plot.figure()
plot.hist(waiting_time)
plot.xlabel('waiting time (min)')
plot.ylabel('no of customers')

plot.figure()
plot.step(obs_times, q_length)
plot.xlabel('time in minutes')
plot.xlabel('queue length')
