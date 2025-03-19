"""
This is a program that shows how to use OOP in the context of Microbit Assignment 9, Game Making.
OOP is used to make a game engine in order to easily manage game events and objects.
"""
from microbit import *
import time
import random
import music

accelerometer.set_range(2)
class Event:
    events_list = []
    
    @staticmethod
    def call_events():
        for event in Event.events_list:
            if event.trigger():
                # Fix this stuff
                if event.max_triggers == "infinite":
                    if isinstance(event.response, (list, tuple)):
                        for response in event.response:
                            response()
                    else:
                        event.response()
                    event.trigger_count += 1
                elif event.trigger_count < event.max_triggers:
                    if isinstance(event.response, (list, tuple)):
                        for response in event.response:
                            response()
                    else:
                        event.response()
                    event.trigger_count += 1
                else:
                    Event.events_list.remove(event)
    
    @staticmethod
    def clear_events():
        Event.events_list = []
    
    def __init__(self, trigger, response, max_triggers="infinite", collect_garbage: bool = True):
        if isinstance(trigger, str):
            triggers = {
                'a': button_a.get_presses,
                'b': button_b.get_presses,
                'aa': button_a.is_pressed,
                'bb': button_b.is_pressed,
                'p0': pin0.is_touched,
                'p1': pin1.is_touched,
                'p2': pin2.is_touched,
                'plogo': pin_logo.is_touched,
                'shake': lambda: accelerometer.was_gesture('shake')
            }
            
            self.trigger = triggers[trigger]
        else:
            self.trigger = trigger
            
        self.response = response
        self.max_triggers = max_triggers
        self.collect_garbage = collect_garbage
        self.trigger_count = 0
        
        Event.events_list.append(self)
    
    def __del__(self):
        if self.collect_garbage:
            Event.events_list.remove(self)
        
    def pause_event(self):
        if self in Event.events_list:
            Event.events_list.remove(self)
    
    def unpause_event(self):
        if self not in Event.events_list:
            Event.events_list.append(self)

class IntervalEvent(Event):
    def __init__(self, ms: int, response, max_triggers="infinite", collect_garbage: bool = True):
        self.ms= ms
        self.previous_time = time.ticks_ms()
        self.current_time = time.ticks_ms()
        self.pause_elapsed = 0
        super().__init__(self.check_time, response, max_triggers, collect_garbage)
    
    def check_time(self):
        self.current_time = time.ticks_ms()
    
        if time.ticks_diff(self.current_time, self.previous_time) + self.pause_elapsed >= self.ms:
            self.previous_time = time.ticks_ms()
            self.current_time = time.ticks_ms()
            self.pause_elapsed = 0
            return True
    
        return False
    
    def pause_event(self):
        if self in Event.events_list:
            Event.events_list.remove(self)
            self.current_time = time.ticks_ms()
            self.pause_elapsed += time.ticks_diff(self.current_time, self.previous_time)
            
    def unpause_event(self):
        if self not in Event.events_list:
            self.previous_time = time.ticks_ms()
            self.current_time = time.ticks_ms()
            Event.events_list.remove(self)

class SettingsPicker:
    def __init__(self, settings_list):
        self.option = 0
        self.selected = False
        self.settings_list = settings_list
        
        display.show(self.option + 1)
        
        self.cycle_event = Event("a", self.change_option)
        self.pick_event = Event("b", self.pick_option)
        
        while not self.selected:
            Event.call_events()
        
        Event.clear_events()
    
    def change_option(self):
        self.option = (self.option + 1) % len(self.settings_list)
        display.show(self.option + 1)
    
    def pick_option(self):
        self.selected = self.settings_list[self.option]

class Screen:
    def __init__(self, frame_rate=10, keep_objects=True, rerender=True):
        self.frame_rate = frame_rate
        self.keep_objects = keep_objects
        self.object_list = []
        self.rerender = rerender
        if self.frame_rate != 0:
            frame_delay = 1000 / self.frame_rate
            self.screen_refresh = IntervalEvent(frame_delay, self.update_screen)  
        
        self.screen = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        
    def __del__(self):
        self.pause()
        self.clear_screen()
        self.update_screen()
    
    def pause(self):
        if self.frame_rate != 0:
            self.screen_refresh.pause_event()
    
    def unpause(self):
        if self.frame_rate != 0:
            self.screen_refresh.unpause_event()
    
    def clear_screen(self):
        self.screen = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    
    def draw_object(self, screen_object):
        if isinstance(screen_object, (list, tuple)):
            for object in screen_object:
                self.draw_object(object)
            
            return
        
        if self.keep_objects and screen_object not in self.object_list:
            self.object_list.append(screen_object)
        
        if not screen_object.updated or self.rerender:
            if not self.rerender:
                # Clear the objects old position
                for x in range(screen_object.x2):
                    for y in range(screen_object.y2):
                        pixel_x = screen_object.old_x1 + x - 1
                        pixel_y = screen_object.old_y1 + y - 1
                        if (pixel_x in range(5)) and (pixel_y in range(5)):
                            self.screen[pixel_y][pixel_x] = 0
            
            # Draw the objects new position
            for x in range(screen_object.x2):
                for y in range(screen_object.y2):
                    pixel_x = screen_object.x1 + x - 1
                    pixel_y = screen_object.y1 + y - 1
                    if pixel_x in range(5) and pixel_y in range(5):
                        self.screen[pixel_y][pixel_x] = screen_object.brightness
            
            screen_object.updated = True
    
    def remove_object(self, screen_object):
        if screen_object in self.object_list:
            self.object_list.remove(screen_object)
        
        # Clear the objects position
        for x in range(screen_object.x2):
            for y in range(screen_object.y2):
                pixel_x = screen_object.x1 + x - 1
                pixel_y = screen_object.y1 + y - 1
                if pixel_x in range(5) and pixel_y in range(5):
                    self.screen[pixel_y][pixel_x] = 0

    def update_screen(self):
        if self.rerender:
            self.clear_screen()
        
        for screen_object in self.object_list:
            self.draw_object(screen_object)
            
        screen_image = Image(":".join(["".join([str(item) for item in row]) for row in self.screen]))
        display.show(screen_image)

class ScreenObject:
    def __init__(self, x1, y1, x2, y2, brightness=9, bounded=False):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.old_x1 = self.x1
        self.old_y1 = self.y1
        self.brightness = brightness
        self.bounded = bounded
        self.updated = False
    
    def change_position(self, x, y):
        position_changed = False
        old_x1 = self.x1
        old_y1 = self.y1
        if self.bounded:
            if (not x > 5 and not x < 1) and (not y > 5 and not y < 1):
                self.x1 = x
                self.y1 = y
                position_changed = True
        else:
            self.x1 = x
            self.y1 = y
            position_changed = True
        
        if position_changed and self.updated:
            self.old_x1 = old_x1
            self.old_y1 = old_y1
            self.updated = False
            
            
    def revert_position(self):
        self.x1 = self.old_x1
        self.y1 = self.old_y1
        self.updated = False
    
    def change_brightness(self, brightness=9):
        self.brightnesss = brightness
    
    def check_collision(self, screen_object):
        if isinstance(screen_object, (list, tuple)):
            for object in screen_object:
                if self.check_collision(object):
                    return True
            
            return False
        
        x3, y3, x4, y4 = (screen_object.x1, screen_object.y1, screen_object.x2, screen_object.y2)
        verticies = (
            (self.x1, self.y1), 
            (self.x1 + self.x2 - 1, self.y1),
            (self.x1 + self.x2 - 1, self.y1 + self.y2 - 1),
            (self.x1, self.y1 + self.y2 - 1)
            )
        
        for x, y in verticies:
            if (x >= x3 and x <= x3 + x4 - 1) and (y >= y3 and y <= y3 + y4 - 1):
                return True
        
        return False



class Player(ScreenObject):
    def __init__(self, x=1, y=3, lives=3):
        super().__init__(x, y, 1, 1, brightness=9, bounded=True)
        self.x = x
        self.y = y
        self.lives = lives
    
    def move_up(self):
        self.change_position(self.x, self.y - 1)
        self.y = self.y1
    
    def move_down(self):
        self.change_position(self.x, self.y + 1)
        self.y = self.y1
    
    # Returns true if the player dies
    def lose_health(self):
        self.lives -= 1
        music.pitch(440, 50, wait=False)
        return self.lives == 0
    
    def is_dead(self):
        return self.lives <= 0

class Asteroid(ScreenObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1, brightness=4)
        self.x = x
        self.y = y
    
    def move_left(self):
        self.x -= 1
        self.change_position(self.x, self.y)

class Wall(ScreenObject):
    def __init__(self, x):
        super().__init__(x, 1, 1, 5)
        self.break_event = Event("shake", self.destroy_wall)
        self.x = x
        self.broken = False
    
    def move_left(self):
        self.x -= 1
        self.change_position(self.x, self.y1)
    
    def destroy_wall(self):
        # How close the wall has to be to the player
        if self.x <= 7:
            self.change_position(self.x, 15)
            music.pitch(659, 100, wait=False)
            self.broken = True
            self.break_event.pause_event()
    
class AsteroidField:
    def __init__(self, screen, starting_speed=400, speed_up=False, wall_gap = 3, gap_after=-1, distribution=[10, 1]):
        self.starting_speed = starting_speed
        self.distribution = distribution
        self.speed_up = speed_up
        self.game_ticks = 0
        self.screen = screen
        self.objects = []
        self.gap = False
        self.wall_gap = wall_gap
        self.gap_after = gap_after
        self.next_wall = False
        
        self.refresh = IntervalEvent(starting_speed, self.update_field)
        
    
    def update_field(self):
        if not self.gap:
            if self.next_wall <= self.gap_after:
                rn = random.randint(1, sum(self.distribution))
                
                if rn <= self.distribution[0]:
                    possible_positions = [1, 2, 3, 4, 5]
                    first_position = random.randint(1, 5)
                    possible_positions.remove(first_position)
                    second_position = possible_positions[random.randint(0, 3)]
                    asteroids = [Asteroid(6, first_position), Asteroid(6, second_position)]
                    self.objects += asteroids
                    self.screen.draw_object(asteroids)
                else:
                    self.next_wall = self.wall_gap
                
                self.gap = True
            elif self.next_wall == 0 :
                wall = Wall(6)
                self.objects.append(wall)
                self.screen.draw_object(wall)
                self.next_wall -= 1
            else:
                self.next_wall -= 1

        else:
            self.gap = False
        
        for object in self.objects:
            if object.x <= -5:
                self.screen.remove_object(object)
                self.objects.remove(object)
                continue
            object.move_left()
        
        self.game_ticks += 1
    
    def clear_field(self):
        for object in self.objects:
            self.screen.remove_object(object)
        
        self.objects = []
    
    def scroll_score(self):
        display.scroll(str(self.game_ticks))
        display.scroll("You died!")
        display.scroll("Your score is " + str(self.game_ticks))


display.scroll("Difficulty?", delay=25)
options = SettingsPicker([
    {"speed": 300, "wall_gap": 3, "gap_after": -1, "distribution": [10, 1], "lives": 2},
    {"speed": 250, "wall_gap": 2, "gap_after": -1, "distribution": [10, 2], "lives": 3},
    {"speed": 200, "wall_gap": 1, "gap_after": -2, "distribution": [10, 3], "lives": 5},
    {"speed": 150, "wall_gap": 0, "gap_after": -1, "distribution": [10, 2], "lives": 1}
    ])
sleep(500)
            
screen = Screen(30)
player = Player(lives=options.selected["lives"])
screen.draw_object(player)
asteroid_field = AsteroidField(
    screen, 
    options.selected["speed"], 
    wall_gap=options.selected["wall_gap"], 
    distribution=options.selected["distribution"], 
    gap_after=options.selected["gap_after"])
player_movement_up = Event("a", player.move_up)
player_movement_down = Event("b", player.move_down)

player_hit = Event(
    lambda: player.check_collision(asteroid_field.objects),
    (
        player.lose_health, 
        asteroid_field.clear_field
        )
    )

player_dead = Event(
    player.is_dead, 
    (
        lambda: screen.remove_object(player),
        screen.clear_screen, 
        asteroid_field.scroll_score
        )
    )

while True:
    Event.call_events() 