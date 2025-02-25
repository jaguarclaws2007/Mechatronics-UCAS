"""
################################################################
Note:

This program does not immediately cut the propellor's power.
Instead, it will initiate the land command, as to avoid
damaging the drone from fall damage. This is preferable 
in most situations.
################################################################
"""

from djitellopy import Tello
tello = Tello()
tello.connect(False)
tello.land()