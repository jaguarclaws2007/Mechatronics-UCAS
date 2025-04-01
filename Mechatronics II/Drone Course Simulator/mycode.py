from Drone_Course_Simulator import Drone

tello = Drone("lh", (400, 400), 0)
tello.rotate_cw(270)
tello.rotate_ccw(270)
tello.forward(300)
tello.launch()
print(tello.command_queue)