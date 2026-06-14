#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
import time
import math

class MyNode(Node):
	def __init__(self):
		super().__init__('scan_demo')
		self.scan_sub = self.create_subscription(LaserScan, 'scan', self.laser_callback, qos_profile_sensor_data)
		time.sleep(10)
		self.laser_ranges = []
		for i in range(360):
			self.laser_ranges.append(0.0)
		self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
		self.cmd = Twist()
		timer_period = 1.0
		self.timer = self.create_timer(timer_period, self.timer_callback)

		
	def PID(self):
		self.cmd.linear.x = 1.0
		self.cmd.angular.z = 0.0
		
	def timer_callback(self):
		self.PID()
		# FIX: Corrected index ranges to stay within 360-degree bounds
		# Front: 0-50 degrees and 310-360 degrees, Left: 50-200 degrees, Right: 160-310 degrees
		front_distance = min(min(self.laser_ranges[0:50]), min(self.laser_ranges[310:360]))
		left_distance = min(self.laser_ranges[50:200])
		right_distance = min(self.laser_ranges[160:310])
		
		self.membership(front_distance, left_distance, right_distance)
		self.cmd.linear.x = self.speedFinal
		self.cmd.angular.z = self.steeringFinal
		self.publisher.publish(self.cmd)
		string = 'Publishing:' + str(self.cmd.linear.x)
		self.get_logger().info(string)
		
	def laser_callback(self, msg):
		self.get_logger().info(str(msg.ranges[90]))
		self.laser_ranges = msg.ranges

		
		
		

	def membership(self, distance1, distance2, distance3):

		self.distance = {}
		self.distance["Near"] = [0.00, 0.00, 0.1, 0.25]
		self.distance["Medium"] = [0.1, 0.25, 0.5]
		self.distance["Far"] = [0.25, 0.5, 10.0, 10.0]
		self.speed = {}
		self.speed["Slow"] = 0.05
		self.speed["Medium"] = 0.15
		self.speed["Fast"] = 0.25
		self.steering = {}
		self.steering["Left"] = 1.0
		self.steering["Zero"] = 0.0
		self.steering["Right"] = -1.0
		self.s01 = 0.0
		self.s02 = 0.0
		self.s11 = 0.0
		self.s12 = 0.0
		self.speedFinal = 0.0
		self.steeringFinal = 0.0


		r1 = {"Near": 100.0, "Medium": 100.0, "Far": 100.0}
		f1 = {"Near": 100.0, "Medium": 100.0, "Far": 100.0}
		valDistance1 = ""
		valDistance2 = ""
		d1 = list(self.distance.values())[0]
		d2 = list(self.distance.values())[1]
		d3 = list(self.distance.values())[2]
		if (distance1 >= list(self.distance.values())[0][1] and distance1 <=
				list(self.distance.values())[0][2]):
			f1["Near"] = 1.0
			valDistance1 = "Near"
		elif (distance1 >= list(self.distance.values())[2][1] and distance1 <=
			  list(self.distance.values())[2][2]):
			f1["Far"] = 1.0
			valDistance1 = "Far"
		elif distance1 == list(self.distance.values())[1][1]:
			f1["Medium"] = 1.0
			valDistance1 = "Medium"
		elif distance1 > list(self.distance.values())[0][2] and distance1 < \
				list(self.distance.values())[0][3]:
			# FIX: Changed 'd' to 'd1'
			f1["Near"] = (d1[3] - distance1) / (d1[3] - d1[2])
			r1["Medium"] = (distance1 - d2[0]) / (d2[1] - d2[0])
			valDistance1 = "Near"
			valDistance2 = "Medium"
		elif distance1 > list(self.distance.values())[1][1] and distance1 < \
				list(self.distance.values())[1][2]:
			f1["Medium"] = (d2[2] - distance1) / (d2[2] - d2[1])
			r1["Far"] = (distance1 - d3[0]) / (d3[1] - d3[0])
			valDistance1 = "Medium"
			valDistance2 = "Far"

		r2 = {"Near": 100.0, "Medium": 100.0, "Far": 100.0}
		f2 = {"Near": 100.0, "Medium": 100.0, "Far": 100.0}
		valDistance3 = ""
		valDistance4 = ""
		d1 = list(self.distance.values())[0]
		d2 = list(self.distance.values())[1]
		d3 = list(self.distance.values())[2]
		if (distance2 >= list(self.distance.values())[0][1] and distance2 <= list(self.distance.values())[0][2]):
			f2["Near"] = 1.0
			valDistance3 = "Near"
		elif (distance2 >= list(self.distance.values())[2][1] and distance2 <= list(self.distance.values())[2][2]):
			f2["Far"] = 1.0
			valDistance3 = "Far"
		elif distance2 == list(self.distance.values())[1][1]:
			f2["Medium"] = 1.0
			valDistance3 = "Medium"
		elif distance2 > list(self.distance.values())[0][2] and distance2 < list(self.distance.values())[0][3]:
			# FIX: Changed 'd' to 'd1'
			f2["Near"] = (d1[3] - distance2) / (d1[3] - d1[2])
			r2["Medium"] = (distance2 - d2[0]) / (d2[1] - d2[0])
			valDistance3 = "Near"
			valDistance4 = "Medium"
		elif distance2 > list(self.distance.values())[1][1] and distance2 < list(self.distance.values())[1][2]:
			f2["Medium"] = (d2[2] - distance2) / (d2[2] - d2[1])
			r2["Far"] = (distance2 - d3[0]) / (d3[1] - d3[0])
			valDistance3 = "Medium"
			valDistance4 = "Far"
			
		r3 = {"Near": 100.0, "Medium": 100.0, "Far": 100.0}
		f3 = {"Near": 100.0, "Medium": 100.0, "Far": 100.0}
		valDistance5 = ""
		valDistance6 = ""
		d1 = list(self.distance.values())[0]
		d2 = list(self.distance.values())[1]
		d3 = list(self.distance.values())[2]
		if (distance3 >= list(self.distance.values())[0][1] and distance3 <= list(self.distance.values())[0][2]):
			f3["Near"] = 1.0
			valDistance5 = "Near"
		elif (distance3 >= list(self.distance.values())[2][1] and distance3 <= list(self.distance.values())[2][2]):
			f3["Far"] = 1.0
			valDistance5 = "Far"
		elif distance3 == list(self.distance.values())[1][1]:
			f3["Medium"] = 1.0
			valDistance5 = "Medium"
		elif distance3 > list(self.distance.values())[0][2] and distance3 < list(self.distance.values())[0][3]:
			# FIX: Changed 'd' to 'd1'
			f3["Near"] = (d1[3] - distance3) / (d1[3] - d1[2])
			r3["Medium"] = (distance3 - d2[0]) / (d2[1] - d2[0])
			valDistance5 = "Near"
			valDistance6 = "Medium"
		elif distance3 > list(self.distance.values())[1][1] and distance3 < list(self.distance.values())[1][2]:
			f3["Medium"] = (d2[2] - distance3) / (d2[2] - d2[1])
			r3["Far"] = (distance3 - d3[0]) / (d3[1] - d3[0])
			valDistance5 = "Medium"
			valDistance6 = "Far"



		x1 = []
		x2 = []
		x3 = []
		s0Val = []
		s1Val = []
		for i in range(27):
			if (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 0:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 1:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Slow")
				s1Val.append("Right")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 2:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Slow")
				s1Val.append("Right")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 3:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 4:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 5:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Medium")
				s1Val.append("Right")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 6:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 7:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Medium")
				s1Val.append("Left")
			elif (valDistance1 == "Near" or valDistance2 == "Near") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 8:
				if f1["Near"] != 100.0:
					x1.append(f1["Near"])
				else:
					x1.append(r1["Near"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 9:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 10:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Slow")
				s1Val.append("Right")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 11:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Slow")
				s1Val.append("Right")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 12:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 13:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 14:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Medium")
				s1Val.append("Right")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 15:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Medium")
				s1Val.append("Left")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 16:
				# FIX: Changed to use Medium for consistency with condition
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Medium")
				s1Val.append("Left")
			elif (valDistance1 == "Medium" or valDistance2 == "Medium") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 17:
				if f1["Medium"] != 100.0:
					x1.append(f1["Medium"])
				else:
					x1.append(r1["Medium"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Medium")
				s1Val.append("Right")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 18:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Zero")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 19:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Slow")
				s1Val.append("Right")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Near" or valDistance4 == "Near") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 20:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Near"] != 100.0:
					x2.append(f2["Near"])
				else:
					x2.append(r2["Near"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Medium")
				s1Val.append("Right")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 21:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 22:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Medium")
				s1Val.append("Zero")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Medium" or valDistance4 == "Medium") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 23:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Medium"] != 100.0:
					x2.append(f2["Medium"])
				else:
					x2.append(r2["Medium"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Medium")
				s1Val.append("Right")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Near" or valDistance6 == "Near") and i == 24:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Near"] != 100.0:
					x3.append(f3["Near"])
				else:
					x3.append(r3["Near"])
				s0Val.append("Slow")
				s1Val.append("Left")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Medium" or valDistance6 == "Medium") and i == 25:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Medium"] != 100.0:
					x3.append(f3["Medium"])
				else:
					x3.append(r3["Medium"])
				s0Val.append("Medium")
				s1Val.append("Left")
			elif (valDistance1 == "Far" or valDistance2 == "Far") and (valDistance3 == "Far" or valDistance4 == "Far") and (valDistance5 == "Far" or valDistance6 == "Far") and i == 26:
				if f1["Far"] != 100.0:
					x1.append(f1["Far"])
				else:
					x1.append(r1["Far"])
				if f2["Far"] != 100.0:
					x2.append(f2["Far"])
				else:
					x2.append(r2["Far"])
				if f3["Far"] != 100.0:
					x3.append(f3["Far"])
				else:
					x3.append(r3["Far"])
				s0Val.append("Fast")
				s1Val.append("Zero")
		for i in range(len(x1)):
			self.s01 = self.s01 + (min(x1[i], x2[i], x3[i]) * self.speed[s0Val[i]])
			self.s02 = self.s02 + min(x1[i], x2[i], x3[i])
			self.s11 = self.s11 + (min(x1[i], x2[i], x3[i]) * self.steering[s1Val[i]])
			self.s12 = self.s12 + min(x1[i], x2[i], x3[i])
			self.speedFinal = self.s01/self.s02
			self.steeringFinal = self.s11/self.s12

		

	
def main(args=None):
	rclpy.init(args=args)
	
	my_node = MyNode()
	rclpy.spin(my_node)
	
	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically when the garbage collector destroys the node object)
	my_node.destroy_node()
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()
