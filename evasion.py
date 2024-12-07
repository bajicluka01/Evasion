class Room:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Sensor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(self.x, self.y)

class Rail:
    def __init__(self, x, y, length, direction):
        self.x = x
        self.y = y
        self.length = length

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


class Complex:
    def __init__(self):
        self.c = 0


#time
t = 0
#number of rails and sensors
nrs = 6

#period
p = -1

#generate arbitrary rails and sensors
rails = []
sensors = []
for i in range(nrs):
    rails.append(Rail(i,i,2,"left"))
    sensors.append(Sensor(i,i))


initial = Configuration(rails, sensors)
initial.print_current()

