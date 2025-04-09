from Drone_Course_Simulator import Drone

tello = Drone("Task 1", (400, 800), 0)
tello.wait(2)
tello.curve(0, 225, 50, -325, 850, 60)
tello.down(50)
tello.forward(100)
tello.backward(100)
tello.right(100)
tello.left(200)
tello.launch()