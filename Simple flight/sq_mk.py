import sys
import time
import math

def navigate_wait(x, y, z, speed, frame_id, tolerance=0.2):
    print navigate(x=x, y=y, z=z, speed=speed, frame_id=frame_id)#

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id=frame_id)
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

def nav(p):
	time.sleep(1)
	print p.x,p.y,p.z

#Input{x,y,z,side of square, angle of rotation}
args = sys.argv[:]

start = Point(int(args[1]), int(args[2]), int(args[3]))
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

print "V",side_v.x,side_v.y,side_v.z
print "V_P",side_v_p.x,side_v_p.y,side_v_p.z
print "CP1",cp1.x,cp1.y,cp1.z
print "CP2",cp2.x,cp2.y,cp2.z
print "CP3",cp3.x,cp3.y,cp3.z

