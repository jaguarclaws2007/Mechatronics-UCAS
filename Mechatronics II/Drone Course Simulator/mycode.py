from Drone_Course_Simulator import Drone

tello = Drone("lh", (400, 400), 0)
tello.forward(100)
tello.curve(23.3, 6.7, 50, -75, 25, 7.9)
print(tello.center_coordinates)
tello.launch()