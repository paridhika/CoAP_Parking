#!/usr/bin/python
import time
import datetime
import random
import threading
import csv
import subprocess
import subprocess
from Queue import Queue
from collections import OrderedDict
from sets import Set
# thread class to run a command
class ExampleThread(threading.Thread):
	def __init__(self,threads,count,sumarray,mean_hold):
		threading.Thread.__init__(self)
		self.threads = threads
		self.count = count
		self.sumarray = sumarray
		self.mean_hold = mean_hold
	def store_time(self,location):
		lockobj.acquire()
		print "get: " + location
		if location in empty_slotsset:
			empty_slotsset.remove(location)
		wait = random.expovariate(self.mean_hold)
		filled_slotsdict[location] = time.time() + wait
		lockobj.release()
	def run(self):
		while(self.count!=0):
			while(self.threads.empty() == False):
				process = self.threads.get()
				self.count -= 1
    				p = subprocess.Popen(process.state, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
				while(True):
		    			out,err = p.communicate()
					if out:
						location = "0,0"
						if len(out.rstrip().splitlines()) > 1:
							location = str(out.rstrip().splitlines()[2])
						self.store_time(location)
					if(p.poll() != None):
		    				end = time.time()
		    				self.sumarray.append(end - process.start_time)
						break;

class ProcessThread(threading.Thread):
	def __init__(self,process,sumarray,mean_hold):
		threading.Thread.__init__(self)
		self.process = process
		self.sumarray = sumarray
		self.mean_hold = mean_hold
	def store_time(self,location):
		lockobj.acquire()
		print "get: " + location
		if location in empty_slotsset:
			empty_slotsset.remove(location)
		wait = random.expovariate(self.mean_hold)
		filled_slotsdict[location] = time.time() + wait
		lockobj.release()
	def run(self):
		p = subprocess.Popen(self.process.state, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		while(True):
    			out,err = p.communicate()
			if out:
				location = "0,0"
				if len(out.rstrip().splitlines()) > 1:
					location = str(out.rstrip().splitlines()[2])
				self.store_time(location)
			if(p.poll() != None):
    				end = time.time()
    				self.sumarray.append(end - self.process.start_time)
				break;

class PutClientThread(threading.Thread):
	def __init__(self,put_mean,mean_hold,count):
		threading.Thread.__init__(self)
		self.put_mean = put_mean
		self.mean_hold = mean_hold
		self.count = count
	def store_time(self,location):
		print "put at: " + location
		wait = random.expovariate(self.mean_hold)
		filled_slotsdict[location] = time.time() + wait
	def run(self):
		f1 = open('Results/run1/60/put_simulation_service_time_60_run1.csv', 'wt')
		f = open('Results/run1/60/put_simulation_result_60_run1.csv', 'wt')
		writer = csv.writer(f)
		service = csv.writer(f1)
		writer.writerow( ('Arrival Rate', 'Service Time','Throughput') )
		service.writerow( ('Mean', 'Count', 'Service Time') )
		sumarray = []
		threads = Queue()
		sum = 0.0;
		for index in range(0,self.count):
			wait = random.expovariate(self.put_mean)
			lockobj.acquire()
			if len(empty_slotsset) != 0:
				location = empty_slotsset.pop()
			else: location = "0,0"
			self.store_time(location)
			lockobj.release()
			state = "xterm -e ./coap-client -m put coap://[::1]/location -e {0} &".format(location)
			start_time = time.time()
			process = ProcessStore(state, start_time)
			thread = ProcessThread(process, sumarray,self.mean_hold)
			thread.start()
			threads.put(thread)
			time.sleep(wait);
		while not threads.empty():
			threads.get().join()
		i = 1
		for val in sumarray:
			service.writerow((self.put_mean , i, val))
			i += 1
			sum += val
		writer.writerow((self.put_mean , sum/self.count, (int)(self.count*3600/sum)))
		f.close()

class GetClientThread(threading.Thread):
	def __init__(self,get_mean,mean_hold,count):
		threading.Thread.__init__(self)
		self.get_mean = get_mean
		self.mean_hold = mean_hold
		self.count = count
	def run(self):
		f1 = open('Results/run1/60/get_simulation_service_time_60_run1.csv', 'wt')
		f = open('Results/run1/60/get_simulation_result_60_run1.csv', 'wt')
		writer = csv.writer(f)
		service = csv.writer(f1)
		writer.writerow( ('Arrival Rate', 'Service Time','Throughput') )
		service.writerow( ('Mean', 'Count', 'Service Time') )
		sumarray = []
		threads = Queue()
		sum = 0.0;
		for index in range(0,self.count):
			wait = random.expovariate(self.get_mean)
			state = "./coap-client -m get coap://[::1]/location &"
			start_time = time.time()
			process = ProcessStore(state, start_time)
			thread = ProcessThread(process, sumarray,self.mean_hold)
			thread.start()
			threads.put(thread)
			time.sleep(wait);
		while not threads.empty():
			threads.get().join()
		i = 1
		for val in sumarray:
			service.writerow((self.get_mean , i, val))
			i += 1
			sum += val
		writer.writerow((self.get_mean , sum/self.count, (int)(self.count*3600/sum)))
		f.close()

class DeleteClientThread(threading.Thread):
	def __init__(self,mean_hold,count):
		threading.Thread.__init__(self)
		self.mean_hold = mean_hold
		self.count = count
	def run(self):
		f1 = open('Results/run1/60/delete_simulation_service_time_60_run1.csv', 'wt')
		f = open('Results/run1/60/delete_simulation_result_60_run1.csv', 'wt')
		writer = csv.writer(f)
		service = csv.writer(f1)
		writer.writerow( ('Arrival Rate', 'Service Time','Throughput') )
		service.writerow( ('Mean', 'Count', 'Service Time') )
		sumarray = []
		arrival_interval = []	#array to store interarrival times of delete processes
		arrival_start = time.time()
		threads = Queue()
		sum = 0.0
		delete_mean = 0.0		#variable to calculate mean interarrival time of delete
		for index in range(0,self.count):
			while any(filled_slotsdict) == False: 
				#print "empty" + str(index) +" " + str(self.count)
				if index >= self.count:
					break
				pass
			sorted_dict = OrderedDict(sorted(filled_slotsdict.items(), key=lambda t: t[1]))
			location,kill_time = sorted_dict.items()[0]
			while kill_time > time.time():
				#print "wait" + str(index)
				pass
			arrival_interval.append(kill_time - arrival_start)
			delete_mean += kill_time - arrival_start
			arrival_start = kill_time
			lockobj.acquire()
			filled_slotsdict.pop(location)
			empty_slotsset.add(location)
			lockobj.release()
			print "delete at: " + location
			state = "xterm -e ./coap-client -m delete coap://[::1]/location -e {0} &".format(location)
			start_time = time.time()
			process = ProcessStore(state, start_time)
			thread = ProcessThread(process, sumarray,self.mean_hold)
			thread.start()
			threads.put(thread)
		while not threads.empty():
			threads.get().join()
		i = 1
		delete_mean /= self.count
		for val in sumarray:
			service.writerow((delete_mean , i, val))
			i += 1
			sum += val
		writer.writerow((delete_mean , sum/self.count, (int)(self.count*3600/sum)))
		f.close()
			
class ProcessStore():
	def __init__(self,state,start_time):
		self.state = state
		self.start_time = start_time
def initEmptySet(empty_slotsset):
	size=100
	for i in range(size):
		for j in range(size):
			empty_slotsset.add(str(i)+","+str(j))

empty_slotsset = set()
filled_slotsdict = OrderedDict()
initEmptySet(empty_slotsset)
lockobj = threading.Lock()
put_mean = 3.415
get_mean = 3.385
mean_hold = 1
count = 1000
put_thread = PutClientThread(put_mean,mean_hold,count)
put_thread.start()
get_thread = GetClientThread(get_mean,mean_hold,count)
get_thread.start()
delete_thread = DeleteClientThread(mean_hold,2*count)
delete_thread.start()
put_thread.join()
delete_thread.join()
get_thread.join()
