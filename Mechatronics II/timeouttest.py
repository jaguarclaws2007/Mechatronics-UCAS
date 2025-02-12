import threading #Imports the threading library
from time import sleep #Imports only the sleep module from the time library
from djitellopy import Tello #Imports only the Tello module from the djitellopy library


def wait(drone, pause_event, stop_event):
    while not stop_event:
        if not pause_event:
            drone.send_rc_control(0, 0, 0, 0)
            print()
            sleep(3)

"""Define items"""
t = Tello() #Create Drone Object
pause_event = threading.Event()
stop_event = threading.Event() #Create a kill flag

waiter = threading.Thread(target = wait, args = (t, pause_event, stop_event), daemon = True)

"""Takeoff"""
t.connect(False) #Create tello drone instance on connected drone port
t.takeoff() #Takeoff!
sleep(2) #Wait for drone to stabilize

"""Position your Drone"""
t.move_forward(100) #Go forward 100 cm

"""Start the keep alive thread"""
waiter.start()  #Execute Process Chain

"""Wait for drones to alllign"""
test = int(input("Num here: ")) #Takes an int input

"Kill and reset keep alive thread"
pause_event.set()

"""Continue with code"""
t.move_back(200) #Go backward 100 cm

pause_event.clear()
test = int(input("Num: "))

stop_event.set()
waiter.join()

t.move_forward(100)
t.land() #Land the drone