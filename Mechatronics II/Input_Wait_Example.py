"""
################################################################
This program is an example of the recommended way to wait for 
long periods of time with the Tello Drones. This is most likely
when long sleeps or waits for user input are needed. The program
uses multithreading to concurrently send a garbage rc control
command that changes the drones motor states by zero. This reaffirms
to the drone that it does indeed exist and has no reason to 
destroy itself after 7 seconds of no response from the control
device. Every line and function has been commented to help explain
usage and for your viewing pleasure. Enjoy...
################################################################
"""
import threading #Imports the threading library
from time import sleep #Imports only the sleep module from the time library
from djitellopy import Tello #Imports only the Tello module from the djitellopy library

"""
Function that waits for user input while using a seperate thread to keep the drone alive
"""
def wait():
    stop = threading.Event() #Set loop exit variable
    def keep_alive(drone, stop): #Keep alive instruction set
        while not stop.is_set(): #while looping
            drone.send_rc_control(0, 0, 0, 0) #Send a garbage command with no expected response
            sleep(3) #Wait 3 seconds
    thread = threading.Thread(target = keep_alive, args=(t, stop), daemon = True) #Create thread instructions
    thread.start() #Initialize Thread
    input() #Wait for user input of anything
    stop.set() #Kill flag variable for while loop
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