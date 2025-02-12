import threading #Imports the threading library
from time import sleep #Imports only the sleep module from the time library
from djitellopy import Tello #Imports only the Tello module from the djitellopy library

"""Create Thread Functions"""
def keep_alive(drone, stop_event):
    """Process function, takes in a drone object and a kill flag"""
    while not stop_event.is_set(): #While flag not raised
        drone.send_rc_control(0, 0, 0, 0)  # Keep drone alive
        print() #Make space for other lines
        sleep(3)  # Send this command every 3 seconds

def stop_keep_alive():
    """Kill thread and reset for next use"""
    stop_event.set() #Raise the kill flag
    keep_alive_thread.join() #Join threads to ensure old process killed
    stop_event.clear() #Reset the kill flag

"""Define items"""
t = Tello() #Create Drone Object
stop_event = threading.Event() #Create a kill flag
keep_alive_thread = threading.Thread(target=keep_alive, args=(t, stop_event), daemon = True) #Create Process Chain

"""Takeoff"""
t.connect(False) #Create tello drone instance on connected drone port
t.takeoff() #Takeoff!
sleep(2) #Wait for drone to stabilize

"""Position your Drone"""
t.move_forward(100) #Go forward 100 cm

"""Start the keep alive thread"""
keep_alive_thread.start()  #Execute Process Chain

"""Wait for drones to alllign"""
test = int(input("Num here: ")) #Takes an int input

"Kill and reset keep alive thread"
stop_keep_alive() #Kills and resets process chain

"""Continue with code"""
t.move_back(100) #Go backward 100 cm
t.land() #Land the drone