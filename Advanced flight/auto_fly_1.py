import rospy
from clever import srv
from std_srvs.srv import Trigger
import sys
import time
import math

from rpi_emg import EMGTelemetryQue, wait_for_command

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
    print navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id=frame_id)
        print telem.z
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            break
        rospy.sleep(0.2)


class Point():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

        def __str__(self):
            s = "Point(" + self.x + " " + self.y + " " + self.z + ")"
            return s

telemetry = EMGTelemetryQue(delay=0.05)

print('Waiting for takeoff')
wait_for_command(telemetry, 'UP', 'UP')

tolerance = 0.2
print navigate(x=0, y=0, z=2, speed=0.2, frame_id="body", auto_arm=True)
rospy.sleep(7)
print "Take off"

tel = get_telemetry(frame_id="aruco_map")
base = Point(tel.x, tel.y, tel.z)

def command(telemetry, pose1, pose2):
    data = telemetry.read()
    telem = get_telemetry(frame_id='body')
    if (data.pose1, data.pose2) == ('SIDE', 'UP'):
        navigate_wait(x=0.5, y=0, z=telem.z, speed=0.5, frame_id='body')
        print('right')
    elif (data.pose1, data.pose2) == ('SIDE', 'DOWN'):
        navigate_wait(x=-0.5, y=0, z=telem.z, speed=0.5, frame_id='body')
        print('left')
    elif (data.pose1, data.pose2) == ('UP', 'SIDE'):
        navigate_wait(x=0, y=0.5, z=telem.z, speed=0.5, frame_id='body')
        print('forward')
    elif (data.pose1, data.pose2) == ('DOWN', 'SIDE'):
        navigate_wait(x=0, y=-0.5, z=telem.z, speed=0.5, frame_id='body')
        print('backward')
    elif (data.pose1, data.pose2) == ('UP', 'DOWN'):
        navigate_wait(x=0, y=0, z=0.5, speed=0.5, frame_id='body')
        print('up')
    elif (data.pose1, data.pose2) == ('DOWN', 'UP'):
        navigate_wait(x=0, y=0, z=-0.5, speed=0.5, frame_id='body')
        print('down')
    elif (data.pose1, data.pose2) == ('UP', 'UP'):
        navigate_wait(x=base.x, y=base.y, z=base.z, speed=0.2, frame_id="aruco_map", auto_arm=False)
        print "Begin landing"
        res = land()
        if res.success:
            print "Perfect landing"


while True:
    comand()
