#!/usr/bin/env python
import rospy
import time
from grid_map_msgs.msg import GridMap  # Import the correct message type

class FrequencyMeasurer:
    def __init__(self, topic_name):
        self.topic_name = topic_name
        self.prev_time = time.time()
        self.msg_count = 0

    def callback(self, msg):
        current_time = time.time()
        self.msg_count += 1

        if self.msg_count >= 10:  # Calculate frequency every 10 messages
            elapsed_time = current_time - self.prev_time
            frequency = self.msg_count / elapsed_time
            print("Frequency: {:.2f} Hz".format(frequency))
            self.msg_count = 0
            self.prev_time = current_time

    def start_measuring(self):
        rospy.Subscriber(self.topic_name, GridMap, self.callback)  # Use GridMap message type
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('frequency_measurer')
    topic = rospy.get_param('~topic')  # Pass the topic name as a parameter
    measurer = FrequencyMeasurer(topic)
    measurer.start_measuring()
