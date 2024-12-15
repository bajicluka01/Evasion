import cv2 as cv
import numpy as np
import keyboard

class Room:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Sensor:
    def __init__(self, rail, color):
        self.rail = rail
        self.color = color

    def print(self):
        print(self.rail.print())

class Rail:
    def __init__(self, x, y, length, direction, color):
        self.x = x
        self.y = y
        self.length = length
        self.color = color

        if direction not in ['left', 'right', 'up', 'down']:
            raise Exception("Incorrect rail direction specified")
        self.direction = direction

    def print(self):
        print(self.x, self.y, self.length, self.direction)

class Configuration:
    def __init__(self, rails, sensors):
        self.rails = rails
        self.sensors = sensors

    def move_all(self):
        print("Executed move")

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
        #grid
        for i in range(0,tmpa):
            cv.line(img, (startx+i*width,starty), (startx+((i+1)*width),starty), (0,0,0), 1)
            for j in range(0,tmpb):
                cv.line(img, (startx+i*width,starty+j*width), (startx+i*width,starty+((j+1)*width)), (0,0,0), 1)
                cv.line(img, (startx+i*width,starty+j*width), (startx+((i+1)*width),starty+(j*width)), (0,0,0), 1)
        cv.line(img, (startx,starty+tmpb*width), (startx+tmpa*width,starty+tmpb*width), (0,0,0), 1)
        cv.line(img, (startx+tmpa*width,starty), (startx+(tmpa*width),starty+(tmpb*width)), (0,0,0), 1)

        #sensors
        for rail in self.rails:
            rectx1 = startx+ (width*(rail.x-1))
            recty1 = starty+ (width*(rail.y-1))
            rectx2 = startx+ (width*(rail.x+1))
            recty2 = starty+ (width*(rail.y+1))
            cv.rectangle(img, (rectx1, recty1), (rectx2, recty2), rail.color, -1)

        return img

    def determine_period(self):
        max_iter = 100000
        initial_state = self.sensors
        period = 0
        for i in range(0,max_iter):
            self.move_all()
            current_state = self.sensors
            if initial_state.equals(current_state):
                return period
            period+=1
        return -1



    def display(self):
        img = self.get_current_image()

        cv.namedWindow("resized_window", cv.WINDOW_NORMAL | cv.WINDOW_KEEPRATIO) 
        cv.resizeWindow("resized_window", 800, 600)
        cv.imshow("resized_window", img)

        while 1==1:
            k = cv.waitKey(0) # Wait for a keystroke in the window
            
            #a to exit
            if k == 97:
                return
            #anything else to execute a move and draw new state
            else:
                self.move_all()
                self.get_current_image()
                cv.destroyAllWindows()
                cv.namedWindow("resized_window", cv.WINDOW_NORMAL | cv.WINDOW_KEEPRATIO) 
                cv.resizeWindow("resized_window", 800, 600)
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
colors = [(0,0,255), (200,0,200), (0,200,0), (255,0,0), (0,255,0), (0,100,200)] #BGR
directions = ["down", "right", "up", "down", "down", "left"]
lengths = [5, 5, 2, 2, 3, 4]
for i in range(nrs):
    rails.append(Rail(locations[i][0],locations[i][1],lengths[i],"left", colors[i]))
    sensors.append(Sensor(rails[i], colors[i]))

initial = Configuration(rails, sensors)
initial.display()

