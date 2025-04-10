from Drone_Course_Simulator import Drone

tello = Drone("Task 1", (300, 150), 180)


#step down code
tello.rotate_ccw(90)
tello.forward(150)
#tello.down(100)
tello.forward(75)
#tello.down(100)
tello.forward(75)
#tello.down(100)
tello.forward(300)
#end left leg

#maze
tello.rotate_ccw(90)
tello.forward(250)
tello.rotate_ccw(90)
tello.forward(100)
tello.rotate_cw(90)
tello.forward(400)
tello.rotate_cw(90)
tello.forward(100)
tello.rotate_ccw(90)
tello.forward(350)

# S Curve
#tello.up(500)
tello.rotate_ccw(90)
tello.forward(100)
#s loop begins
tello.forward(50)
#tello.up(300)
tello.rotate_ccw(180)
tello.forward(50)
tello.rotate_ccw(180)
#s loop ends
tello.forward(150)
for i in range(10):
    tello.rotate_ccw(9)
    tello.forward(59)
tello.forward(600)

#time.sleep(10000)
#tello.rotate(90)
#tello.forward(100)
#tello.curve(23.3, 6.7, 50, -75, 25, 7.9)
#print(tello.center_coordinates)
tello.launch()
