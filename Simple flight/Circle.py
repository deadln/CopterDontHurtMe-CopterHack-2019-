import rospy
from clever import srv
from std_srvs.srv import Trigger
import sys
import time
import math

rospy.init_node('circle_flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def navigate_wait(x, y, z, speed, frame_id, tolerance=0.2):
    print navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id)#

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id=frame_id)
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            break
        rospy.sleep(0.2)

navigate_wait(x=0,y=0,z=2,speed=0.2,frame_id="body")
tel = get_telemetry(frame_id="aruco_map")
base = Point(tel.x,tel.y,tel.z)
navigate_wait(x=start.x,y=start.y,x=start.z,speed=0.3,frame_id="aruco_map")
rospy.wait(2)
