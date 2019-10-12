#import rospy
#from clever import srv
#from std_srvs.srv import Trigger
import sys #sys.argv
import time
from Point import Point

def get_points():
    user_args = sys.argv[1:]
    points_arr = []
    point = [0, 0, 0]
    counter = 0

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
    return points_arr


a = get_points()


def nav(p):
    time.sleep(1)
    print p.x, p.y, p.z


start = Point(1, 2, 2)

nav(Point(0, 0, 2))

nav(start)

cycles = 1

for i in range(cycles):
    for p in a:
        nav(p)

    nav(Point(0, 0, 2))


##################################
    
def navigate(x=0, y=0, z=0, speed=0, frame_id=0):
    print(x, y, z, speed, frame_id)
        
    
def takeoff_wait(alt, speed=0.5, tolerance=0.2):
    start = get_telemetry()
    navigate(z=alt, speed=speed, frame_id='body', auto_arm=True)

    while not rospy.is_shutdown():
        if get_telemetry().z - start.z + z < tolerance:
            break

        rospy.sleep(0.2)


def navigate_wait(x, y, z, speed, frame_id, tolerance=0.2):
    start = get_telemetry()
    #print navigate(z=alt, speed=speed, frame_id='body', auto_arm=True)

    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id=frame_id)
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            break
        rospy.sleep(0.2)

def land_wait():
    land()
    while get_telemetry().armed:
        rospy.sleep(0.2)