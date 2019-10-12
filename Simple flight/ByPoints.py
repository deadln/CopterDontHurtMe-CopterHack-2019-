import rospy
from clever import srv
from std_srvs.srv import Trigger
import sys #sys.argv
import time
from Point import Point
from math 

        

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
        

def get_points():
    user_args = sys.argv[1:]
    points_arr = []
    point = [0, 0, 0]
    counter = 0
    cycles = 1

    for i in range(len(user_args)):
        flag = 1
        if flag:
            try:
                arg = int(user_args[i])
                point[counter] = arg
                counter += 1
                if counter == 3:
                    counter = 0
                    points_arr.append(Point(point[0], point[1], point[2]))
            except:
                flag = 0
                continue
        cycles = user_args[i]

    print navigate(x=0, y=0, z=2, speed=0.2, frame_id="body", auto_arm = True)
    rospy.sleep(7)

    print "Take off"
    tel = get_telemetry(frame_id="aruco_map")
    base = Point(tel.x, tel.y, tel.z)

    for i in cycles:
        for point in points_arr:
            print navigate_wait(x=point.x, y=point.y, z=point.z, speed=0.2, frame_id="aruco_map", auto_arm=False)
            print "Passed"

    navigate_wait(x=base.x, y=base.y, z=base.z, speed=0.2, frame_id="aruco_map", auto_arm=False)
    print "Begin landing"

    res = land()
    if res.success:
        print "Perfect landing"
