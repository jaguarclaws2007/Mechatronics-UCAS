from Drone_Course_Simulator import Drone

tello = Drone("Task4", (1300, 650), 0)

# S Curve
#tello.up(500)
tello.rotate_ccw(90)
#s loop begins
tello.forward(50)
#tello.up(300)
tello.rotate_ccw(180)
tello.forward(50)
tello.rotate_ccw(180)
#s loop ends

#curve
tello.forward(150)
for i in range(10):
    tello.rotate_ccw(9)
    tello.forward(59)

tello.forward(500)

tello.launch()