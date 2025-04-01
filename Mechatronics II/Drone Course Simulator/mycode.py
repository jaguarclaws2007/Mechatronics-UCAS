from Drone_Course_Simulator import Drone

tello = Drone("lh", (400, 400), 0)
tello.rotate_cw(270)
tello.rotate_ccw(270)
tello.wait(2)
tello.forward(300)
tello.launch()