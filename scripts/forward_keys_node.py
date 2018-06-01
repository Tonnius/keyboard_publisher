#!/usr/bin/env python

import rospy
from keyboard_publisher.key_listener import KeyListener
from geometry_msgs.msg import TwistStamped
from keyboard_publisher.msg import KeyEvent
from std_msgs.msg import String

class KeyForwarder(KeyListener):
    def __init__(self):
        KeyListener.__init__(self)
        self.key_forward_pub = rospy.Publisher('panda_movegroup/keyboard', String, queue_size=1)
        rospy.Subscriber("keyboard_publisher/key_event", KeyEvent, self.callback)

    def callback(self, key_event_msg):
        if key_event_msg.pressed:           
            self.key_forward_pub.publish(key_event_msg.char)

if __name__ == '__main__':
    try:
        rospy.init_node("forward_keys_node")
        rate = rospy.Rate(100)
        key_publisher = KeyForwarder()

        while not rospy.is_shutdown():
            rate.sleep()

    except rospy.ROSInterruptException:
        pass
