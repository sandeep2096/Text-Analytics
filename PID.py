#!/user/bin/env python
import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data



class Minimalsubscriber(Node):
	def __init__(self):
            super().__init__('forward_demo')
            self.scan_sub = self.create_subscription(LaserScan, 'scan', self.laser_callback, qos_profile_sensor_data)
            self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
            self.cmd  = Twist()
            timer_period = 0.5
            self.timer = self.create_timer(timer_period, self.timer_callback)
            self.i = 0
            self.kp = 0.5	
            self.ki = 0.0001		
            self.kd = 0.02
            self.e=0
            self.desired_distance = 0.3
            self.ei = 0
            self.ed = 0
            self.e_previous = 0
		
		
	def PID(self):
            self.current_distance=min(self.laser_ranges[880:1100])
            self.error = self.desired_distance - self.current_distance
            self.ei = self.ei + self.e
            self.ed = self.e - self. e_previous
            angular_velocity = self.kp * self.e + self.ki * self.ei + self.kd * self.ed
            self.e_previous = self.e
            self.cmd.linear.x = 0.2
            self.cmd.angular.z = angular_velocity
           
	 	
	def timer_callback(self):
            self.PID()
            self.publisher_.publish(self.cmd)
            string = 'publishing' + str(self.cmd.linear.x)
            self.get_logger().info(string)
		
	def laser_callback(self, msg):
            self.get_logger().info(str(msg.ranges[90]))
            self.laser_ranges = msg.ranges
           
def main(args=None):
        rclpy.init(args=args)
    
        minimal_subscriber = Minimalsubscriber()
        rclpy.spin(minimal_subscriber)
	
        minimal_publisher.destroy_node()
        rclpy.shutdown()


if __name__=='__main__':
        main()





 


	
