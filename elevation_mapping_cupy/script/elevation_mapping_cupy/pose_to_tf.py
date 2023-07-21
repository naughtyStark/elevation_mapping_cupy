#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import tf

pose_pub = rospy.Publisher("/pose", PoseWithCovarianceStamped, queue_size = 10)

def pose_cb(msg):
    br = tf.TransformBroadcaster()
    pos = msg.pose.position
    rot = msg.pose.orientation
    br.sendTransform((pos.x, pos.y, pos.z),
                     (rot.x, rot.y, rot.z, rot.w),
                     msg.header.stamp,
                     "base_link",
                     "map")

    br.sendTransform((0.15, 0.0, 0.1),
                     (0, 0, 0, 1),
                     msg.header.stamp,
                     "camera_depth_frame",
                     "base_link")

    br.sendTransform((0, 0, 0),
                     (-0.5, 0.5, -0.5, 0.5),
                     msg.header.stamp,
                     "camera_depth_optical_frame",
                     "camera_depth_frame")


    pose = PoseWithCovarianceStamped()
    pose.pose.pose.position = msg.pose.position
    pose.pose.pose.orientation = msg.pose.orientation
    pose.header.stamp = msg.header.stamp
    pose.header.frame_id = msg.header.frame_id
    pose_pub.publish(pose)


if __name__ == '__main__':
    rospy.init_node('tf_broadcaster')
    rospy.Subscriber('/mavros/local_position/pose', PoseStamped, pose_cb)

    rospy.spin()