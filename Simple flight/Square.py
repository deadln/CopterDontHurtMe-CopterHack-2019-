#import rospy
#from clever import srv
#from std_srvs.srv import Trigger
import sys
import time

#rospy.init_node('square_flight')

#get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
#navigate = rospy.ServiceProxy('navigate', srv.Navigate)
#navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
#set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
#set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
#set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
#set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
#land = rospy.ServiceProxy('land', Trigger)

#def navigate_wait(x, y, z, speed, frame_id, tolerance=0.2):
#    navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id)#
#
#    while not rospy.is_shutdown():
#        telem = get_telemetry(frame_id=frame_id)
#        if get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
#            break
#        rospy.sleep(0.2)

class Point():
    def __init__(self,x,y,z):
    	self.x = x
    	self.y = y
    	self.z = z

	def __str__(self):
		s = "Point(" + self.x + " " + self.y + " " + self.z + ")"
		return s

def nav(p):
	time.sleep(1)
	print p.x,p.y,p.z

args = sys.argv[:]

for i in range(len(args)):
    #s = int(ar[i]) * -1
    print args[i]

start = Point(int(args[1]), int(args[2]), int(args[3]))
side = int(args[4])
cq = int(args[5])
cycles = int(args[6])
cp1, cp2, cp3 = 0,0,0
if cq == 1:
	cp1 = Point(start.x, start.y + side, start.z)
	cp2 = Point(start.x + side, start.y + side, start.z)
	cp3 = Point(start.x + side, start.y, start.z)
elif cq == 2:
	cp1 = Point(start.x + side, start.y, start.z)
	cp2 = Point(start.x + side, start.y - side, start.z)
	cp3 = Point(start.x, start.y - side, start.z)
elif cq == 3:
	cp1 = Point(start.x, start.y - side, start.z)
	cp2 = Point(start.x - side, start.y - side, start.z)
	cp3 = Point(start.x - side, start.y, start.z)
elif cq == 4:
	cp1 = Point(start.x - side, start.y, start.z)
	cp2 = Point(start.x - side, start.y + side, start.z)
	cp3 = Point(start.x, start.y + side, start.z)
else:
	cp1 = Point(start.x, start.y + side, start.z)
	cp2 = Point(start.x + side, start.y + side, start.z)
	cp3 = Point(start.x + side, start.y, start.z)

print start.x,start.y,start.z
print cp1.x,cp1.y,cp1.z
print cp2.x,cp2.y,cp2.z
print cp3.x,cp3.y,cp3.z

print "Taking off"
nav(Point(0,0,2))

nav(start)

for i in range(cycles):
	nav(cp1)
	nav(cp2)
	nav(cp3)
	nav(start)
	print
	
nav(Point(0,0,2))
#land()
