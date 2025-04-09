from Drone_Course_Simulator import Drone

tello = Drone("Task 1", (200, 200), 0)

#tello.curve(50, 6.7, 30, 20, 25, 7.9)
#tello.down(50)
tello.backward(100)
tello.launch()