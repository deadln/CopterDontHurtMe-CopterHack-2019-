import rospy
from clever import srv
from std_srvs.srv import Trigger

import math

rospy.init_node('test')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def get_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def navigate_wait(x, y, z, speed, frame_id, tolerance=0.2):
    print navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id)#

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id=frame_id)
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            break
        rospy.sleep(0.2)

print navigate(x=0,y=0,z=2,speed=0.2,frame_id="body", auto_arm=True)
rospy.sleep(7)
print "Take off"

navigate_wait(0,0,2,0.2,"aruco_77")
print 'Finish'
rospy.sleep(4)

print "Success"

res = land()

if res.success:
        print "success"



