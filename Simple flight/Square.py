
import rospy
from clever import srv
from std_srvs.srv import Trigger
import sys
import time
import math

rospy.init_node('square_flight')

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


def navigate_wait(x, y, z, speed, frame_id, auto_arm):
    tolerance = 0.2
    print navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm = auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id=frame_id)
        print telem.z
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            break
        rospy.sleep(0.2)

class Point():
    def __init__(self,x=0,y=0,z=0):
        self.x = x
        self.y = y
        self.z = z

        def __str__(self):
                s = "Point(" + self.x + " " + self.y + " " + self.z + ")"
                return s

#Input{x,y,z,side of square, angle of rotation}
args = sys.argv[:]

start = Point(float(args[1]), float(args[2]), float(args[3]))
side = int(args[4])
a = float(int(args[5]) % 360) * (math.pi / 180)
cycles = int(args[6])

#Vector
side_v = Point(side * math.cos(a), side * math.sin(a), 0)
#Vector turned 90 right
side_v_p = Point(side * math.cos(a + 4.71239), side * math.sin(a + 4.71239),0)



cp1 = Point(start.x + side_v.x, start.y + side_v.y, start.z)
cp2 = Point(cp1.x + side_v_p.x, cp1.y + side_v_p.y, start.z)
cp3 = Point(cp2.x - side_v.x, cp2.y - side_v.y, start.z)


tolerance = 0.2
print navigate(x=0, y=0, z=2, speed=0.2, frame_id="body", auto_arm = True)
rospy.sleep(7)

print "Take off"
tel = get_telemetry(frame_id="aruco_map")
base = Point(tel.x,tel.y,tel.z)
navigate_wait(x=start.x,y=start.y,z=start.z,speed=0.2,frame_id="aruco_map", auto_arm=False)
print "On position"
#Main cycle
for i in range(cycles):
        navigate_wait(x=cp1.x,y=cp1.y,z=cp1.z,speed=0.2,frame_id="aruco_map", auto_arm=False)
        print "CP1"
        navigate_wait(x=cp2.x,y=cp2.y,z=cp2.z,speed=0.2,frame_id="aruco_map", auto_arm=False)
        print "CP2"
        navigate_wait(x=cp3.x,y=cp3.y,z=cp3.z,speed=0.2,frame_id="aruco_map", auto_arm=False)
        print "CP3"     
        navigate_wait(x=start.x,y=start.y,z=start.z,speed=0.2,frame_id="aruco_map", auto_arm=False)
        print "START"   
        print

#Returning to base
navigate_wait(x=base.x,y=base.y,z=base.z,speed=0.2,frame_id="aruco_map", auto_arm=False)
print "Begin landing"
res = land()

if res.success:
        print "Perfect landing"

