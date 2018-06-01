#!/usr/bin/env python

import rospy
from keyboard_publisher.key_listener import KeyListener
from geometry_msgs.msg import TwistStamped
from keyboard_publisher.msg import KeyEvent
from std_msgs.msg import String

class BrainToTwist():
    def __init__(self):
        self.twist_pub = rospy.Publisher('jog_arm_server/delta_jog_cmds', TwistStamped, queue_size=1)
        rospy.Subscriber("chatter", String, self.callback) #listen for commands coming from OpenVibe
        self.twist_msg = TwistStamped()

    def callback(self, openvibe_msg):
        #print openvibe_msg.data
        self.twist_msg.header.stamp = rospy.Time.now()

        self.twist_msg.twist.linear.x = 0
        self.twist_msg.twist.linear.y = 0
        self.twist_msg.twist.linear.z = 0
        self.twist_msg.twist.angular.x = 0
        self.twist_msg.twist.angular.y = 0
        self.twist_msg.twist.angular.z = 0

        if openvibe_msg.data == "3": #left
            self.twist_msg.twist.linear.y = 0.2
            self.twist_pub.publish(self.twist_msg)

        if openvibe_msg.data == "2": #right
            self.twist_msg.twist.linear.y = -0.2
            self.twist_pub.publish(self.twist_msg)
        if openvibe_msg.data == "1": #up
            self.twist_msg.twist.linear.z = 0.2
            self.twist_pub.publish(self.twist_msg)

        if openvibe_msg.data == "4": #down
            self.twist_msg.twist.linear.z = -0.2
            self.twist_pub.publish(self.twist_msg)

if __name__ == '__main__':
    try:
        rospy.init_node("brain_to_twist_node")
        rate = rospy.Rate(100)
        key_publisher = BrainToTwist()

        while not rospy.is_shutdown():
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
