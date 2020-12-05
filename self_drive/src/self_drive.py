#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:

    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        turtle_vel = Twist()
        
        if 0 < scan.ranges[0] < 0.25 or 0 < scan.ranges[30] < 0.25 or 0 < scan.ranges[-30] < 0.25:
            turtle_vel.angular.z = -1.8
        elif abs(scan.ranges[110] - scan.ranges[70]) > 0.02 and (scan.ranges[110] - scan.ranges[70]) > 0 or \
                0 < scan.ranges[90] < 0.1:
            turtle_vel.angular.z = -0.7
            turtle_vel.linear.x = 0.18
        elif abs(scan.ranges[110] - scan.ranges[70]) > 0.02 and (scan.ranges[110] - scan.ranges[70]) < 0 or \
                scan.ranges[90] > 0.2:
            turtle_vel.angular.z = 0.7
            turtle_vel.linear.x = 0.18
        else:
            turtle_vel.linear.x = 0.18
                
        self.publisher.publish(turtle_vel)
    
def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()

