import threading
import time


class MyThread(threading.Thread):
	
	x_distance = 0
	y_distance = 0
		
		
	def __init__(self, name, x_distance,  y_distance):
		super(MyThread, self).__init__()
		print("called constructor of Super class")
		self.x_distance = x_distance
		self.y_distance = y_distance
				
		
	def run(self):
		print("{0} has started!".format(self.getName()))
		print("Rotate servo {0} with angle = {1}".format(self.y_distance, self.x_distance))
		time.sleep(1)
		print("{0} has finished!".format(self.getName()))

def add():
	thread_id  = threading.get_ident()
	print('id = {0}'.format(thread_id))
	number = 0
	for i in range(1, 10):
		number = number + 10
	return number

if __name__ == '__main__':	
	for i in range(10):
		t = MyThread(name = "Thread - {0}".format(i + 1), x_distance=i, y_distance = i * 10)
		t.start()
		time.sleep(.9)
	