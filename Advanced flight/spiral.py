from math import *
import rospy
from clever import srv
from std_srvs.srv import Trigger
from math import *



rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)





def get_distance(x1, y1, z1, x2, y2, z2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def navigate_wait(x, y, z, speed, frame_id, auto_arm):
    tolerance = 0.2
    print navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id, auto_arm = auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id=frame_id)
        print telem.z
        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
            break
        rospy.sleep(0.2)





def spiral(x, y, start_z, end_z, start_r, end_r, alpha_delta, iter_amount):
    x = float(x);
    y = float(y);
    start_z = float(start_z);
    end_z = float(end_z);
    start_r = float(start_r);
    end_r = float(end_r);
    aplha_delta = float(alpha_delta);
    iter_amount = float(iter_amount)
    mass = list()
    for i in range(int(iter_amount + 1)):
        mass.append([])
    alpha = 0
    x0 = x
    y0 = y
    z0 = start_z
    z = z0
    counter_1 = 0
    #k = 1
    if start_r < end_r and end_r - start_r != 0:
        for r in range(int(start_r * iter_amount), int(end_r * iter_amount + 1), int(end_r - start_r)):

            x = (r * sin(alpha) + x0) / iter_amount
            y = (r * cos(alpha) + y0) / iter_amount
            z = (z + (end_z - start_z) / iter_amount)
            mass[counter_1].append(x)
            mass[counter_1].append(y)
            mass[counter_1].append(z)
            alpha += alpha_delta
            counter_1 += 1

    elif (end_r - start_r == 0):
        for r in range(int(iter_amount)+1):
            x = (r * sin(alpha) + x0) / iter_amount
            y = (r * cos(alpha) + y0) / iter_amount
            z = (z + (end_z - start_z) / iter_amount)
            mass[counter_1].append(x)
            mass[counter_1].append(y)
            mass[counter_1].append(z)
            alpha += alpha_delta
            counter_1 += 1
    return mass

massive = spiral(x=0, y=0, start_z=0, end_z=1, start_r=1, end_r=2, alpha_delta=0.5, iter_amount=30)

navigate(x = 0, y = 0, z = 2, speed = 0.2, frame_id = 'body', auto_arm = True)

rospy.sleep(7)

tel = get_telemetry(frame_id="aruco_map")
base = Point(tel.x, tel.y, tel.z)


for i in range(len(massive)):
    navigate_wait(x = massive[i][0]+5, y = massive[i][1]+5, z = massive[i][2]+2, speed = 0.1, frame_id = 'aruco_map', auto_arm = False)

rospy.sleep(2)
navigate_wait(x=base.x, y=base.y, z=base.z, speed=0.2, frame_id="aruco_map", auto_arm=False)
print "Begin landing"

res = land()
if res.success:
    print "Perfect landing"