import threading #Imports the threading library
from time import sleep #Imports only the sleep module from the time library
from djitellopy import Tello #Imports only the Tello module from the djitellopy library

"""
Function that waits for user input while using a seperate thread to keep the drone alive
"""
def wait():
    stop = False #Set loop exit variable
    def keep_alive(drone, stop): #Keep alive instruction set
        while not stop: #while looping
            drone.send_rc_control(0, 0, 0, 0) #Send a garbage command with no expected response
            sleep(3) #Wait 3 seconds
    thread = threading.Thread(target = keep_alive, daemon = True) #Create thread instructions
    thread.start() #Initialize Thread
    input() #Wait for user input of anything
    stop = True #Kill flag variable for while loop
    thread.join() #Wait for thread to finish processing before continuing main program

"""Startup"""
t = Tello() #Create Drone Object
t.connect(False) #Create tello drone instance on connected drone port
t.takeoff() #Takeoff!
sleep(2) #Wait for drone to stabilize

"""Position your Drone"""
t.move_forward(100) #Go forward 100 cm

"""Wait for drones to align"""
wait() #Waits for user input while keeping drone alive

"""Continue with code"""
t.move_back(200) #Go backward 100 cm

"""Wait for drones to align"""
wait() #Waits for user input while keeping drone alive

"""Continue with code"""
t.move_forward(100) #Go forward 100 cm
t.land() #Land the drone