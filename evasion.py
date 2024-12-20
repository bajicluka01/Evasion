import cv2 as cv
import numpy as np

class Room:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Sensor:
    def __init__(self, center, rail, direction, color):
        self.x = center[0]
        self.y = center[1]
        self.rail = rail
        self.color = color

        if direction not in ['left', 'right', 'up', 'down']:
            raise Exception("Incorrect rail direction specified")
        self.direction = direction

    def print(self):
        print(self.rail.print())

class Rail:
    def __init__(self, start, end, length, color):
        self.start = start
        self.end = end
        self.length = length
        self.color = color

    def print(self):
        print(self.start, self.end, self.length)

class Configuration:
    def __init__(self, rails, sensors):
        self.rails = rails
        self.sensors = sensors

    def copy(self):
        return Configuration(self.rails, self.sensors)

    def sensor_values(self):
        vals = []
        for sensor in self.sensors:
            vals.append((sensor.x, sensor.y))
        return vals

    def move_all(self):
        newsensors = []
        for rail, sensor in zip(self.rails, self.sensors):
            if sensor.direction == "left":
                if sensor.x == rail.start[0]:
                    sensor.x = rail.start[0]
                    sensor.direction = "right"
                else:
                    sensor.x-=1
            if sensor.direction == "right":
                if sensor.x == rail.end[0]:
                    sensor.x = rail.end[0]-1 #doesn't work if stationary rails
                    sensor.direction="left"
                else:
                    sensor.x+=1
            if sensor.direction == "up":
                if sensor.y == rail.start[1]:
                    sensor.y = rail.start[1]
                    sensor.direction="down"
                else:
                    sensor.y-=1
            if sensor.direction == "down":
                if sensor.y == rail.end[1]:
                    sensor.y = rail.end[1]-1 #doesn't work if stationary rails
                    sensor.direction="up"
                else:
                    sensor.y+=1
            
            newsensors.append(sensor)
        self.sensors = newsensors


    def print_current(self):
        for rail in self.rails:
            print(rail.print())

        for sensor in self.sensors:
            print(sensor.print())

    def get_current_image(self):
        img = np.zeros([500,500,3],dtype=np.uint8)
        img.fill(255)
        startx = 5
        starty = 5
        tmpa = 8
        tmpb = 8
        width = 50

        #sensors
        for sensor in self.sensors:
            rectx1 = startx+ (width*(sensor.x-1))
            recty1 = starty+ (width*(sensor.y-1))
            rectx2 = startx+ (width*(sensor.x+1))
            recty2 = starty+ (width*(sensor.y+1))
            cv.rectangle(img, (rectx1, recty1), (rectx2, recty2), sensor.color, -1)

        #grid
        for i in range(0,tmpa):
            cv.line(img, (startx+i*width,starty), (startx+((i+1)*width),starty), (0,0,0), 1)
            for j in range(0,tmpb):
                cv.line(img, (startx+i*width,starty+j*width), (startx+i*width,starty+((j+1)*width)), (0,0,0), 1)
                cv.line(img, (startx+i*width,starty+j*width), (startx+((i+1)*width),starty+(j*width)), (0,0,0), 1)
        cv.line(img, (startx,starty+tmpb*width), (startx+tmpa*width,starty+tmpb*width), (0,0,0), 1)
        cv.line(img, (startx+tmpa*width,starty), (startx+(tmpa*width),starty+(tmpb*width)), (0,0,0), 1)

        #rails
        for rail in self.rails:
            linestartx = startx+ (width * rail.start[0])
            linestarty = starty+ (width * rail.start[1])
            lineendx = startx+ (width * rail.end[0])
            lineendy = starty+ (width * rail.end[1])
            cv.line(img, (linestartx, linestarty), (lineendx, lineendy), rail.color, 4)

        return img

    def equals(self, first, second):
        if len(first) != len(second):
            return False

        for a, b in zip(first, second):
            if a!=b:
                return False
        return True

    def determine_period(self):
        max_iter = 100000
        configuration = self.copy()
        initial_state = configuration.sensor_values()
        period = 1
        for i in range(0,max_iter):
            configuration.move_all()
            current_state = configuration.sensor_values()
            if self.equals(initial_state, current_state):
                return period
            period+=1
        raise Exception("Couldn't determine period: exceeded ", max_iter, " iterations.")

    def display(self):
        img = self.get_current_image()
        cv.namedWindow("resized_window", cv.WINDOW_NORMAL) 
        cv.resizeWindow("resized_window", 800, 800)
        cv.imshow("resized_window", img)

        while 1==1:
            k = cv.waitKey(0)
            
            #a to exit
            if k == 97:
                return
            #anything else to execute a move and draw new state
            else:
                self.move_all()
                img = self.get_current_image()
                #cv.destroyAllWindows()
                #cv.namedWindow("resized_window", cv.WINDOW_NORMAL) 
                #cv.resizeWindow("resized_window", 800, 800)
                cv.imshow("resized_window", img)

class Complex:
    def __init__(self):
        self.c = 0

    def complement(self):
        return 0

#time
t = 0
#number of rails and sensors
nrs = 6

#period
p = -1

#generate rails and sensors
rails = []
sensors = []
locations = [(1,1), (6,1), (5,4), (3,5), (7,5), (4,7)]
railcolors = [(0,0,255), (200,0,200), (0,200,0), (255,0,0), (0,255,0), (0,100,200)] #BGR
sensorcolors = [(0,0,230), (200,0,170), (0,170,0), (230,0,0), (0,230,0), (0,100,170)] #BGR
directions = ["down", "right", "down", "up", "down", "left"]
lengths = [5, 5, 2, 2, 3, 4]
railstarts = [(1,1), (2,1), (5,3), (3,3), (7,3), (1,7)]
railends =   [(1,6), (7,1), (5,5), (3,5), (7,7), (5,7)]
for i in range(nrs):
    rails.append(Rail(railstarts[i], railends[i], lengths[i], railcolors[i]))
    sensors.append(Sensor(locations[i], rails[i], directions[i], sensorcolors[i]))

initial = Configuration(rails, sensors)
initial.display()
print(initial.determine_period())
