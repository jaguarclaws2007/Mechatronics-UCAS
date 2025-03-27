'''Libraries'''
import pygame
import math
import csv
import os
from random import randint
pygame.init()

'''Shape Classes'''
class arc_object(object):
    def __init__(self, id, x1, y1, x2, y2, color, layer, surface):
        self.blockchain_id = id
        self.type = 'arc'
        self.layer = layer
        self.x = 0
        self.y = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        x3 = (x1 + x2) / 2 + 20
        y3 = (y1 + y2) / 2
        self.x3 = x3
        self.y3 = y3
        self.color = color
        self.surface = surface
        self.hitbox = (x1, y1, x2, y2)
        self.expansion_hitbox_1 = (x1 - 10, y1 - 10, 20, 20)
        self.expansion_hitbox_2 = (x2 - 10, y2 - 10, 20, 20)
        self.expansion_hitbox_3 = (x3 - 10, y3 - 10, 20, 20)
        self.can_lock = True
        self.locked = False
        self.start_angle = 0
        self.end_angle = 0
        self.selector_angle = 0

    def adjust_selector_point(self):
        offset = 1e-4  # Adjusting offset to prevent overlapping coordinates
        if self.x3 == self.x1:
            self.x3 += offset
        elif self.x3 == self.x2:
            self.x3 -= offset
        if self.y3 == self.y1:
            self.y3 += offset
        elif self.y3 == self.y2:
            self.y3 -= offset

    def circumcircle_calc(self):
        self.adjust_selector_point()
        y1, y2, y3 = -self.y1, -self.y2, -self.y3
        self.mid_x_1 = (self.x1 + self.x3) / 2
        self.mid_y_1 = (y1 + y3) / 2
        self.mid_x_2 = (self.x2 + self.x3) / 2
        self.mid_y_2 = (y2 + y3) / 2

        try:
            self.slope_1 = round((y3 - y1) / (self.x3 - self.x1), 6)
            if self.slope_1 != 0:
                self.slope_1_I = - (1 / self.slope_1)
                self.int_1_I = self.mid_y_1 - self.slope_1_I * self.mid_x_1
        except ZeroDivisionError:
            self.slope_1_I = 0

        try:
            self.slope_2 = round((y3 - y2) / (self.x3 - self.x2), 6)
            if self.slope_2 != 0:
                self.slope_2_I = - (1 / self.slope_2)
                self.int_2_I = self.mid_y_2 - self.slope_2_I * self.mid_x_2
        except ZeroDivisionError:
            self.slope_2_I = 0

        if self.slope_2 == 0:
            self.x_I = self.mid_x_2
        elif self.slope_1 == 0:
            self.x_I = self.mid_x_1
        else:
            self.x_I = (self.int_1_I - self.int_2_I) / (self.slope_1_I - self.slope_2_I)

        if self.slope_1 == 0:
            self.y_I = self.slope_2_I * self.x_I - self.int_2_I
        else:
            self.y_I = self.slope_1_I * self.x_I - self.int_1_I

        self.x_I = -self.x_I
        self.radius = math.sqrt(((self.x1 - self.x_I) ** 2) + ((y1 + self.y_I) ** 2))

        self.circumcircle_hitbox = (self.x_I - self.radius, (self.y_I - self.radius), self.radius * 2, self.radius * 2)

    def distance_to_line(self, x0, y0, x1, y1, x2, y2):
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return numerator / denominator if denominator != 0 else float('inf')


    def is_point_on_arc(self, center_x, cy, start_angle, end_angle, px, py):
        # Calculate the angle of the point (px, py) relative to the center (cx, cy)
        angle_point = math.atan2(py - cy, px - center_x)

        # Normalize the angles to be between [0, 2π]
        if start_angle < 0:
            start_angle += 2 * math.pi
        if end_angle < 0:
            end_angle += 2 * math.pi
        if angle_point < 0:
            angle_point += 2 * math.pi

        # Ensure the angles are in correct order (start_angle to end_angle) on the circle
        if start_angle > end_angle:
            start_angle, end_angle = end_angle, start_angle  # swap if needed for the arc's direction

        # Check if the angle of the point lies between start_angle and end_angle
        if start_angle <= angle_point <= end_angle:
            return True
        return False
    
    def draw(self):
        threshold = 10  # Distance threshold to switch from arc to line
        distance = self.distance_to_line(self.x3, self.y3, self.x1, self.y1, self.x2, self.y2)

        # Update hitboxes
        self.hitbox = (self.x1 + self.x, self.y1 + self.y, self.x2 + self.x, self.y2 + self.y)
        self.expansion_hitbox_1 = (self.x1 + self.x - 10, self.y1 + self.y - 10, 20, 20)
        self.expansion_hitbox_2 = (self.x2 + self.x - 10, self.y2 + self.y - 10, 20, 20)
        self.expansion_hitbox_3 = (self.x3 + self.x - 10, self.y3 + self.y - 10, 20, 20)

        if distance < threshold and self.can_lock:
            self.locked = True
            # If the selector is close to the line, draw a straight line
            self.mid_x_main = (self.x1 + self.x2) / 2
            self.mid_y_main = (self.y1 + self.y2) / 2
            self.x3 = self.mid_x_main
            self.y3 = self.mid_y_main
            pygame.draw.line(self.surface, self.color, 
                             (self.x1 + self.x, self.y1 + self.y), 
                             (self.x2 + self.x, self.y2 + self.y), 5)
        elif not self.can_lock or not (distance < threshold):
            self.locked = False
            try:
                # Calculate Circumcircle
                self.circumcircle_calc()            

                # Calculate angles for the points
                theta1 = math.atan2(self.y2 - self.y_I, self.x2 - self.x_I)
                theta2 = math.atan2(self.y1 - self.y_I, self.x1 - self.x_I)
                theta3 = math.atan2(self.y3 - self.y_I, self.x3 - self.x_I)

                # Invert the angles to match Pygame's y-axis
                self.start_angle = -theta1
                self.end_angle = -theta2
                self.selector_angle = -theta3

                # Normalize Angles
                if self.start_angle < 0:
                    self.start_angle += 2 * math.pi
                if self.end_angle < 0:
                    self.end_angle += 2 * math.pi
                if self.selector_angle < 0:
                    self.selector_angle += 2 * math.pi
                if self.start_angle > self.end_angle:
                    self.start_angle, self.end_angle = self.end_angle, self.start_angle

                # Swap if necessary
                if not (self.start_angle < self.selector_angle < self.end_angle):
                    self.start_angle, self.end_angle = self.end_angle, self.start_angle

                # Construct Arc
                pygame.draw.arc(self.surface, self.color, 
                                    (self.x_I - self.radius, self.y_I - self.radius, self.radius * 2, self.radius * 2), 
                                    self.start_angle, self.end_angle, 1)
            except ZeroDivisionError:
                pass
            
        
        # Draw hitboxes
        pygame.draw.rect(self.surface, "yellow", self.expansion_hitbox_1, 2)
        pygame.draw.rect(self.surface, "yellow", self.expansion_hitbox_2, 2)
        pygame.draw.ellipse(self.surface, "yellow", self.expansion_hitbox_3, 2)

        

class ellipse_object(object):
    def __init__(self, id, x, y, width, height, color, layer, surface):
        self.blockchain_id = id
        self.type = 'ellipse'
        self.layer = layer
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = surface
        self.hitbox = (x - width / 2, y - height / 2, width, height)
        self.expansion_hitbox = (x + width / 2, y - (height / 2) - 20, 20, 20)
    
    def draw(self):
        self.hitbox = (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.expansion_hitbox = (self.x + self.width / 2, self.y - (self.height / 2) - 20, 20, 20)
        pygame.draw.ellipse(self.surface, self.color, self.hitbox)
        pygame.draw.rect(self.surface, "yellow", self.expansion_hitbox, 2)

class rectangle_object(object):
    def __init__(self, id, x, y, width, height, color, layer, surface):
        self.blockchain_id = id
        self.type = 'rectangle'
        self.layer = layer
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.surface = surface
        self.hitbox = (x - width / 2, y - height / 2, width, height)
        self.expansion_hitbox = (x + width / 2, y - (height / 2) - 20, 20, 20)

    def draw(self):
        self.hitbox = (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.expansion_hitbox = (self.x + self.width / 2, self.y - (self.height / 2) - 20, 20, 20)
        pygame.draw.rect(self.surface, self.color, self.hitbox)
        pygame.draw.rect(self.surface, "yellow", self.expansion_hitbox, 2)

class drone(object):
    def __init__(self, map_name):
        self.map_name = map_name

'''Detection'''
def hitbox(hitbox_stationary, hitbox_mobile):
    if hitbox_mobile[0] >= hitbox_stationary[0] and hitbox_mobile[0] + hitbox_mobile[2] <= hitbox_stationary[0] + hitbox_stationary[2]:
        if hitbox_mobile[1] >= hitbox_stationary[1] and hitbox_mobile[1] + hitbox_mobile[3] <= hitbox_stationary[1] + hitbox_stationary[3]:
            return True
    return False

def hitline(hitbox_stationary, hitbox_mobile):
    try:
        slope = (hitbox_stationary[1]- hitbox_stationary[3]) / (hitbox_stationary[0] - hitbox_stationary[2])
        b = hitbox_stationary[1] - (slope * hitbox_stationary[0])
        greater = max(hitbox_stationary[0], hitbox_stationary[2])
        lesser = min(hitbox_stationary[0], hitbox_stationary[2])
        if (abs(hitbox_mobile[1] - (slope * hitbox_mobile[0] + b)) <= abs(8 * (1 + abs(slope)))) and (lesser <= hitbox_mobile[0] <= greater):
            return True
    except ZeroDivisionError:
        if abs(hitbox_mobile[0] - hitbox_stationary[0]) <= 8:
            return True
    return False

def hitarc(stationary_hitbox, mobile_hitbox):
    mx, my, mw, mh = mobile_hitbox
    center_x, center_y, radius, start_angle, stop_angle = stationary_hitbox

    corners = [
        (mx, my),  # Top-left corner
        (mx + mw, my),  # Top-right corner
        (mx, my + mh),  # Bottom-left corner
        (mx + mw, my + mh)  # Bottom-right corner
    ]

    for corner in corners:
        corner_x, corner_y = corner
        # Find the angle of the corner relative to the center of the arc
        angle = -math.atan2(corner_y - center_y, corner_x - center_x)
        if angle < 0:
            angle += 2 * math.pi  # Normalize angle
        
        # Check if the corner is within the angular bounds of the arc and within the radius
        distance_squared = (corner_x - center_x)**2 + (corner_y - center_y)**2
        if start_angle < angle < stop_angle and distance_squared <= radius**2:
            return True  # Collision detected (corner inside arc)

    # No collision detected
    return False

def hitellipse(hitbox_stationary, hitbox_mobile):
    x_test = hitbox_mobile[0]
    y_test = -hitbox_mobile[1]
    width = hitbox_stationary[2]
    height = hitbox_stationary[3]
    x_center = hitbox_stationary[0] + width / 2
    y_center = -(hitbox_stationary[1] + height / 2)
    x_axis = (width / 2) ** 2
    y_axis = (height / 2) ** 2
    
    test = (((x_test - x_center) ** 2) / x_axis) + (((y_test - y_center) ** 2) / y_axis)
    if test <= 1:
        return True
    return False

def hitborder(hitbox):
    """
    Checks to see if border has been overstepped by a shape or its expansion hitbox
    if it has, it moves the shape back to the border
    """
    x = 0
    y = 0
    hit = False
    left_x = hitbox[0]
    right_x = hitbox[0] + hitbox[2]
    top_y = hitbox[1]
    bottom_y = hitbox[1] + hitbox[3]
    if left_x < newX: x = newX - left_x
    elif right_x > main_screen_size_x: x = main_screen_size_x - right_x
    if top_y < 0: y = -top_y
    elif bottom_y > main_screen_size_y: y = main_screen_size_y - bottom_y
    
    if y != 0 or x != 0:
        hit = True
    changes = (x, y, hit)
    return(changes)

'''Start Variables'''
#Main Screen starting constants
start_flag = True
main_screen_size_x = 750
main_screen_size_y = 750
main_screen = pygame.display.set_mode((main_screen_size_x, main_screen_size_y), pygame.RESIZABLE)
background_color = (0, 33, 130)
accent_color = (236, 206, 247)
blueprint_spacing = 25
menu_width = 100
tab_height = 85
newX = menu_width + 1

#Gametime starting constants
game_font = pygame.freetype.SysFont("Arial", 30)
saved = False
exit_flag = False
running = True
dt = 0
clock = pygame.time.Clock()
times_averaged = 0
average_fps = 0

#Inputs starting constants
pygame.mouse.set_cursor(pygame.cursors.arrow)
hit = False
mouse_lock = (False, None, None, None, 0, 0) #lock, object, mouse_x, mouse_y
main_screen_x_center = main_screen_size_x / 2
main_screen_y_center = main_screen_size_y / 2
x_mouse = main_screen_x_center
y_mouse = main_screen_y_center
mouse_hitbox = (x_mouse, y_mouse, 0, 0)
pygame.mouse.set_pos(x_mouse, y_mouse)
mouse_layer = 1
snap_mode = False
selected_blockchain_id = 0
obstacles = ()

#Objects starting constants
shape_id_blockchain = 0
shape_lock = (False, None, None)
shape_blockchain_ids = {}
moving = False
altering_point_1 = False
altering_point_2 = False
altering_point_3 = False
expanding = False
can_select = True
select_countdown = 0
class menu_icon(object):
    def __init__(self, path, mount_coordinates, scale_factor, highlight_color, screen, job_function):
        self.path = path
        self.mount_coordinates = mount_coordinates
        self.scale_factor = scale_factor
        self.highlight_color = highlight_color
        self.screen = screen
        self.job_function = job_function

        self.icon = pygame.image.load(self.path).convert_alpha()
        self.icon_width = self.icon.get_size()[0]
        self.icon_height = self.icon.get_size()[1]
        self.final_size = (int(self.icon_width * self.scale_factor), int(self.icon_height * self.scale_factor))
        self.icon_final = pygame.transform.scale(self.icon, self.final_size)

        self.hitbox = (self.mount_coordinates[0], self.mount_coordinates[1], self.final_size[0], self.final_size[1])

    def draw(self):
        self.screen.blit(self.icon_final, (self.mount_coordinates[0], self.mount_coordinates[1]))

    def action(self):
        self.job_function()

def save_map():
    save_options_popup.execute = True

def exit_creator():
    global running, exit_flag
    if saved:
        running = False
    else:
        exit_flag = True

def copy_shape():
    global shape_id_blockchain
    global selected_blockchain_id
    global mouse_layer
    
    oobj = shape_blockchain_ids.get(selected_blockchain_id) #original object
    if oobj.type == "arc":
        copied_obstacle = arc_object(shape_id_blockchain, oobj.x1 - 50, oobj.y1 + 50, oobj.x2 - 50, oobj.y2 + 50, oobj.color, shape_id_blockchain + 1, oobj.surface)
        copied_obstacle.x3 - 50
        copied_obstacle.y3 + 50
    elif oobj.type == "rectangle":
        copied_obstacle = rectangle_object(shape_id_blockchain, oobj.x - 50, oobj.y + 50, oobj.width, oobj.height, oobj.color, shape_id_blockchain + 1, oobj.surface)
    elif oobj.type == "ellipse":
        copied_obstacle = ellipse_object(shape_id_blockchain, oobj.x - 50, oobj.y + 50, oobj.width, oobj.height, oobj.color, shape_id_blockchain + 1, oobj.surface)

    shape_blockchain_ids[copied_obstacle.blockchain_id] = copied_obstacle
    selected_blockchain_id = shape_id_blockchain
    mouse_layer = shape_id_blockchain + 1
    shape_id_blockchain += 1


def delete_shape():
    shape_blockchain_ids.pop(selected_blockchain_id, None)

def up_layer():
    global mouse_layer
    obstacle = shape_blockchain_ids.get(selected_blockchain_id)
    higher_obstacle = None
    for obj in shape_blockchain_ids.values():
        if obj.layer == obstacle.layer + 1:
            higher_obstacle = shape_blockchain_ids.get(obj.blockchain_id)
            higher_obstacle.layer -= 1
            obstacle.layer += 1
            break
    if higher_obstacle == None:
        obstacle.layer += 1
    mouse_layer += 1
    

def down_layer():
    global mouse_layer
    obstacle = shape_blockchain_ids.get(selected_blockchain_id)
    lower_obstacle = None
    if obstacle.layer == 1:
        return
    else:
        for obj in shape_blockchain_ids.values():
            if obj.layer == obstacle.layer -1:
                lower_obstacle = shape_blockchain_ids.get(obj.blockchain_id)
                lower_obstacle.layer += 1
                obstacle.layer -= 1
                break
        if lower_obstacle == None:
            obstacle.layer -= 1
        mouse_layer -= 1

def add_arc():
    global shape_id_blockchain
    global selected_blockchain_id
    global mouse_layer
    new_arc = arc_object(shape_id_blockchain, main_screen_x_center, main_screen_y_center, main_screen_x_center + 50, main_screen_y_center + 50, "cyan", shape_id_blockchain + 1, main_screen)
    shape_blockchain_ids[new_arc.blockchain_id] = new_arc
    selected_blockchain_id = shape_id_blockchain
    mouse_layer = shape_id_blockchain + 1
    shape_id_blockchain += 1

def add_square():
    global shape_id_blockchain
    global selected_blockchain_id
    global mouse_layer
    new_rectangle = rectangle_object(shape_id_blockchain, main_screen_x_center, main_screen_y_center, 75, 75, "green", shape_id_blockchain + 1, main_screen)
    shape_blockchain_ids[new_rectangle.blockchain_id] = new_rectangle
    selected_blockchain_id = shape_id_blockchain
    mouse_layer = shape_id_blockchain + 1
    shape_id_blockchain += 1


def add_ellipse():
    global shape_id_blockchain
    global selected_blockchain_id
    global mouse_layer
    new_ellipse = ellipse_object(shape_id_blockchain, main_screen_x_center, main_screen_y_center, 100, 100, "purple", shape_id_blockchain + 1, main_screen)
    shape_blockchain_ids[new_ellipse.blockchain_id] = new_ellipse
    selected_blockchain_id = shape_id_blockchain
    mouse_layer = shape_id_blockchain + 1
    shape_id_blockchain += 1

save_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/save.png", (19.5, 12), 3.8125, "green", main_screen, save_map)
exit_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/exit.png", (19.5, 607), 3.8125, "green", main_screen, exit_creator)
copy_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/copy.png", (19.5, 437), 3.8125, "green", main_screen, copy_shape)
delete_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/delete.png", (19.5, 522), 3.8125, "green", main_screen, delete_shape)
up_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/up.png", (12, 352), 3.81255, "green", main_screen, up_layer)
down_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/down.png", (57, 352), 3.81255, "green", main_screen, down_layer)
arc_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/line.png", (19.5, 97), 3.81255, "green", main_screen, add_arc)
square_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/square.png", (19.5, 182), 3.81255, "green", main_screen, add_square)
ellipse_icon = menu_icon("Mechatronics II/Drone Course Simulator/Assets/ellipse.png", (19.5, 267), 3.81255, "green", main_screen, add_ellipse)

menu_icons = [save_icon, exit_icon, copy_icon, delete_icon, up_icon, down_icon, arc_icon, square_icon, ellipse_icon]

#Exit popup
exit_popup_width, exit_popup_height = 300, 200
exit_popup = pygame.Surface((exit_popup_width, exit_popup_height))
exit_popup.fill((200, 200, 200))
exit_popup_x, exit_popup_y = (main_screen_size_x - exit_popup_width) / 2, (main_screen_size_y - exit_popup_height) / 2

title_font = pygame.font.Font(None, 48)
info_font = pygame.font.SysFont("Arial", 28)

class Button(object):
    def __init__(self, screen, text, x_center, y_center, width, height, color, highlight_color, text_color):
        self.screen = screen
        self.text = text
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.color = color
        self.highlight_color = highlight_color
        self.text_color = text_color

        self.locator_rect = pygame.Rect(x_center - width / 2, y_center - height / 2, width, height)
        self.projecting_screen = pygame.Surface((width, height))
        self.rendered_text = info_font.render(text, True, text_color)
        self.text_width = self.rendered_text.get_rect()[2]
        self.text_height = self.rendered_text.get_rect()[3]
        self.text_rect = ((width - self.text_width) / 2, (height - self.text_height) / 2, self.text_width, self.text_height)

    def draw(self):
        self.projecting_screen.fill(self.color)
        self.projecting_screen.blit(self.rendered_text, self.text_rect)
        self.screen.blit(self.projecting_screen, self.locator_rect)
        if hitbox(self.locator_rect, mouse_hitbox):
            pygame.draw.rect(main_screen, self.highlight_color, (self.locator_rect[0] - 2, self.locator_rect[1] - 2, self.locator_rect[2] + 4, self.locator_rect[3] + 4), 2)

    def is_clicked(self):
        global can_select
        if hitbox(self.locator_rect, mouse_hitbox):
            if can_select and left_click:
                can_select = False
                return True
        else:
            return False


def render_wrapped_text(text, font, color, text_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        # Check width if this word is added
        if font.size(test_line)[0] <= text_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Add the last line
    if current_line:
        lines.append(current_line)

    line_surfaces = [font.render(line, True, color) for line in lines]
    line_height = font.get_linesize()
    text_height = line_height * len(line_surfaces)

    # Create a surface to hold all lines
    text_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)

    # Blit each line onto the text_surface
    for i, line_surface in enumerate(line_surfaces):
        text_surface.blit(line_surface, (0, i * line_height))

    return text_surface


class popup(object):
    def __init__(self, screen, x_center, y_center, width, height, text, color, highlight_color, text_color):
        self.screen = screen
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.highlight_color = highlight_color
        self.text_color = text_color

        self.locator_rect = pygame.Rect(x_center - width / 2, y_center - height / 2, width, height)
        self.projecting_screen = pygame.Surface((width, height))
        self.execute = True

        self.rendered_text = render_wrapped_text(text, info_font, text_color, width - 20)


    def draw(self):
        self.projecting_screen.fill(self.color)
        self.projecting_screen.blit(self.rendered_text, (10, 10))
        self.screen.blit(self.projecting_screen, self.locator_rect)
import time
class ScrollMenu:
    def __init__(self, x, y, width, height, font, item_list, scroll_speed=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.item_list = item_list
        self.scroll_speed = scroll_speed
        self.scroll_offset = 0
        self.last_scroll_time = time.time()  # Track the last scroll time

    def handle_scroll_event(self, event):
        """Handle scroll events with delta time."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll("up")
            elif event.button == 5:  # Scroll down
                self.scroll("down")

    def handle_selection_event(self, event):
        """Handle item selection on click."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
                selected_index = (mouse_y - self.y) // 40 - 1  # Find which item was clicked
                if 0 <= selected_index < len(self.item_list):
                    selected_file = self.item_list[selected_index]
                    return selected_file  # Return selected item
        return None

    def draw(self, screen):
        """Draw the scrollable menu."""
        pygame.draw.rect(screen, "white", (self.x, self.y, self.width, self.height))
        
        # Draw the items in the list with scrolling
        for i, item in enumerate(self.item_list[self.scroll_offset:]):
            y_position = self.y + 20 + i * 40  # Adjust spacing between items
            if y_position > self.y + self.height:
                break
            item_text = self.font.render(item, True, "black")
            screen.blit(item_text, (self.x + 10, y_position))

    def scroll(self, direction):
        """Scroll the menu list with delta time."""
        current_time = time.time()
        delta_time = dt  # Get time difference between scroll events
        
        if delta_time < 0.1:  # Prevent too rapid scrolling
            return  # Avoid updating scroll offset if the scroll is too quick
        
        if direction == "down" and self.scroll_offset + self.scroll_speed < len(self.item_list):
            self.scroll_offset += self.scroll_speed
        elif direction == "up" and self.scroll_offset - self.scroll_speed >= 0:
            self.scroll_offset -= self.scroll_speed
        
        self.last_scroll_time = current_time  # Update the last scroll time

class TextBox:
    def __init__(self, x, y, width, height, font, color, bg_color, max_length=50):
        # Initialize the position, size, font, color, etc.
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle for the text box
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.max_length = max_length  # Maximum number of characters allowed
        self.text = ""  # Text inside the box
        self.final_text = ""
        self.submit = False
        self.active = False  # Determines whether the text box is active for typing
        self.cursor_pos = len(self.text)  # Keeps track of where the cursor is in the text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is inside the box
            if self.rect.collidepoint(event.pos):
                self.active = True  # Set the text box as active
            else:
                self.active = False  # Deactivate if clicked outside
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    # Handle backspace (delete last character)
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    # Handle enter (optional: can do something with the entered text)
                    self.submit = True
                elif len(self.text) < self.max_length and event.unicode.isprintable():
                    # Add character to text if it's printable and within max length
                    self.text += event.unicode

    def draw(self, screen):
        if self.submit:
            self.final_text = self.text
            self.active = False
        # Draw the text box with its background
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Border color
        
        # Render the text
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        # Optionally, draw the cursor if the text box is active
        if self.active and pygame.time.get_ticks() % 1000 < 500:  # Blink every 500ms
            # Calculate the cursor's position after the last character
            cursor_x = self.rect.x + 5 + self.font.size(self.text)[0]  # The width of the text
            cursor_y = self.rect.y + (self.rect.height - self.font.get_height()) // 2
            pygame.draw.line(screen, self.color, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font.get_height()), 2)

def exit_action_popup():
    global running
    global exit_flag
    showing = True
    while showing and running:
        critical_events()
        main_screen_background()
        main_screen_menu()
        get_user_inputs()
        draw_obstacles()
        exit_popup.fill((200, 200, 200))  # Clear previous renders
        game_font.render_to(exit_popup, (10, 10), "Test", (0, 0, 0))  # Black text at position (50, 80)
        main_screen.blit(exit_popup, (exit_popup_x, exit_popup_y))
        gametime_runner()

def critical_events():
    global main_screen_size_x
    global main_screen_size_y
    global running
    global current_file

    '''Critical Events'''
    selected_file = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWRESIZED:
            main_screen_size_x, main_screen_size_y = pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]
        text_box.handle_event(event)
        text_box_2.handle_event(event)
        

def main_screen_background():
    '''Background and Grid lines'''
    main_screen.fill(background_color)
    for i in range(newX + blueprint_spacing, main_screen_size_x + 1, blueprint_spacing):
        pygame.draw.line(main_screen, accent_color, (i, 0), (i, main_screen_size_y))
    for i in range(0, main_screen_size_y + 1, blueprint_spacing):
        pygame.draw.line(main_screen, accent_color, (newX, i), (main_screen_size_x, i))

def main_screen_menu():
    '''Menu'''
    pygame.draw.rect(main_screen, "black", (0, 0, menu_width, main_screen_size_y))
    for i in range(9):
        pygame.draw.line(main_screen, "white", (0, i * tab_height), (menu_width, i * tab_height))
    pygame.draw.line(main_screen, "white", (menu_width, 0), (menu_width, main_screen_size_y))

    for icon in menu_icons:
        icon.draw()

change_x_count = 0
change_y_count = 0


def snap_mode_correct(x_coord, y_coord):
    if (x_coord - newX) % blueprint_spacing >= blueprint_spacing / 2:
        x_coord += blueprint_spacing - ((x_coord - newX) % blueprint_spacing)
    elif (x_coord - newX) % blueprint_spacing < blueprint_spacing / 2 and (x_coord - newX) % blueprint_spacing != 0:
        x_coord -= (x_coord - newX) % blueprint_spacing

    if (y_coord) % blueprint_spacing >= blueprint_spacing / 2:
        y_coord += blueprint_spacing - y_coord % blueprint_spacing
    elif y_coord % blueprint_spacing < blueprint_spacing / 2 and y_coord % blueprint_spacing != 0:
        y_coord -= y_coord % blueprint_spacing
    
    return (x_coord, y_coord)


def get_user_inputs():
    global keys
    global running
    global snap_mode
    global old_x
    global old_y
    global mouse_hitbox
    global left_click
    global change_x
    global change_y
    global x_mouse
    global y_mouse
    global change_x_count
    global change_y_count

    '''Keyboard Input'''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        running = False
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        snap_mode = True
    else:
        snap_mode = False

    '''Mouse Calculations'''
    old_x = x_mouse
    old_y = y_mouse
    x_mouse, y_mouse = pygame.mouse.get_pos()
    mouse_hitbox = (x_mouse, y_mouse, 0, 0)
    left_click = list(pygame.mouse.get_pressed())[0]

    change_x = x_mouse - old_x
    change_y = y_mouse - old_y
    if snap_mode:
        change_x_count += change_x
        change_y_count += change_y
        if abs(change_x_count) >= blueprint_spacing:
            change_x = change_x_count
            change_x_count = 0
        else:
            change_x = 0
        if abs(change_y_count) >= blueprint_spacing:
            change_y = change_y_count
            change_y_count = 0
        else:
            change_y = 0

def draw_obstacles():
    '''Drawing Shapes'''
    global obstacles
    obstacles = sorted(shape_blockchain_ids.values(), key = lambda x: x.layer)
    for shape in obstacles:
        shape.draw()

def gametime_runner():
    '''Gametime Runner'''
    global select_countdown
    global can_select
    global dt
    global times_averaged
    global average_fps

    if not can_select:
        select_countdown += dt
    if select_countdown >= 0.75:
        select_countdown = 0
        can_select = True

    pygame.display.flip()
    dt = clock.tick() / 1000
    times_averaged += 1
    if times_averaged == 0:
        average_fps = clock.get_fps()
    else:
        average_fps += (clock.get_fps() - average_fps) / times_averaged

start_read = "Welcome to the Tello drone simulator. Add shapes and obstacles and place them wherever you want. Hold SHIFT while moving to move in set increments."
counter = 0
spup = popup(main_screen, main_screen_x_center, main_screen_y_center, 400, 300, start_read, "black", "green", "white")
sbutton = Button(main_screen, "Get Started", main_screen_x_center, (spup.locator_rect[0] + spup.locator_rect[3]), 150, 100, "grey", "white", "black")

start_read_2 = "Would you like to coninue working on an old course, or start a new one?"
spup2 = popup(main_screen, main_screen_x_center, main_screen_y_center, 400, 200, start_read_2, "black", "green", "white")
sbutton2 = Button(main_screen, "New Course", main_screen_x_center - 125, (spup2.locator_rect[1] + spup2.locator_rect[3] - 35), 150, 70, "grey", "white", "black")
sbutton3 = Button(main_screen, "Edit Course", main_screen_x_center + 125, (spup2.locator_rect[1] + spup2.locator_rect[3] - 35), 150, 70, "grey", "white", "black")
spup2.execute = False

new_course_read = "Enter the name for your course"
new_course_popup = popup(main_screen, main_screen_x_center, main_screen_y_center, 400, 200, new_course_read, "black", "green", "white")
text_box = TextBox(new_course_popup.locator_rect[0], new_course_popup.locator_rect[1] + 80, 400, 40, info_font, "black", "white")
new_course_finish_button = Button(main_screen, "Finish", main_screen_x_center, (new_course_popup.locator_rect[1] + new_course_popup.locator_rect[3] - 35), 150, 70, "grey", "white", "black")
new_course_popup.execute = False

edit_course_read = "Enter the name for the course you would like to edit"
edit_course_popup = popup(main_screen, main_screen_x_center, main_screen_y_center, 400, 300, edit_course_read, "black", "green", "white")
all_files = os.listdir("Mechatronics II/Drone Course Simulator/Saved Maps")
text_box_2 = TextBox(new_course_popup.locator_rect[0], new_course_popup.locator_rect[1] + 80, 400, 40, info_font, "black", "white")
edit_course_finish_button = Button(main_screen, "Finish", main_screen_x_center, (new_course_popup.locator_rect[1] + new_course_popup.locator_rect[3] - 35), 150, 70, "grey", "white", "black")
edit_course_popup.execute = False

save_options_text = "Would you like to save this map under its old name, or save as a new one?"
save_options_popup = popup(main_screen, main_screen_x_center, main_screen_y_center, 400, 200, save_options_text, "black", "green", "white")
save_options_popup.execute = False
save_button = Button(main_screen, "Save", main_screen_x_center - 125, (save_options_popup.locator_rect[1] + save_options_popup.locator_rect[3] - 35), 150, 70, "grey", "white", "black")
save_as_button = Button(main_screen, "Save As", main_screen_x_center + 125, (save_options_popup.locator_rect[1] + save_options_popup.locator_rect[3] - 35), 150, 70, "grey", "white", "black")

saving_popup = popup(main_screen, main_screen_x_center, main_screen_y_center, 200, 100, "Saving", "black", "green", "white")
saving_popup.execute = False

def save_current_course():
    # Open the CSV file in write mode
    with open(current_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write headers to the CSV file
        writer.writerow(['Key', 'ID', 'Type', 'Layer', 'X', 'Y'])

        # Loop through each item in the obstacle_dict
        for key, obj in shape_blockchain_ids.items():

            if isinstance(obj, arc_object):
                # Collect common attributes
                data = [
                    key,                # ID (key in dictionary)
                    obj.blockchain_id,
                    obj.type,
                    obj.layer,
                    obj.x,
                    obj.y,
                    obj.x1,
                    obj.y1,
                    obj.x2,
                    obj.y2,
                    obj.x3,
                    obj.y3,
                    obj.color,
                    obj.surface,
                    obj.hitbox,
                    obj.expansion_hitbox_1,
                    obj.expansion_hitbox_2,
                    obj.expansion_hitbox_3,
                    obj.can_lock,
                    obj.locked,
                    obj.start_angle,
                    obj.end_angle,
                    obj.selector_angle   
                    ]

            else:
                data = [
                    key,                # ID (key in dictionary)
                    obj.blockchain_id,           # Type (arc, ellipse, or rect)
                    obj.type,             # x1
                    obj.layer,             # y1
                    obj.x,             # x2
                    obj.y,             # y2
                    obj.width,          # color
                    obj.height,          # layer
                    obj.color,
                    obj.surface,
                    obj.hitbox,
                    obj.expansion_hitbox
                    ]

            # Write the row to the CSV file
            writer.writerow(data)


def process_file_load(file):
     global mouse_layer
     global shape_id_blockchain
     global selected_blockchain_id


     with open(file, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        """new_arc = arc_object(shape_id_blockchain, main_screen_x_center, main_screen_y_center, main_screen_x_center + 50, main_screen_y_center + 50, "cyan", shape_id_blockchain + 1, main_screen)
            shape_blockchain_ids[new_arc.blockchain_id] = new_arc"""

        for row in reader:
            if row[2] == "arc":
                new_arc = arc_object(int(row[1]), float(row[6]), float(row[7]), float(row[8]), float(row[9]), row[12], int(row[3]), main_screen)
                new_arc.x3 = float(row[10])
                new_arc.y3 = float(row[11])
                shape_blockchain_ids[int(row[0])] = new_arc

                selected_blockchain_id = int(row[0])
                mouse_layer = shape_id_blockchain + 1
                shape_id_blockchain += 1


            elif row[2] == "rectangle":
                new_rectangle = rectangle_object(int(row[1]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), row[8], int(row[3]), main_screen)
                shape_blockchain_ids[int(row[0])] = new_rectangle

                selected_blockchain_id = int(row[0])
                mouse_layer = shape_id_blockchain + 1
                shape_id_blockchain += 1

            elif row[2] == "ellipse":
                new_ellipse = ellipse_object(int(row[1]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), row[8], int(row[3]), main_screen)
                shape_blockchain_ids[int(row[0])] = new_ellipse

                selected_blockchain_id = int(row[0])
                mouse_layer = shape_id_blockchain + 1
                shape_id_blockchain += 1


current_file = None






class Propellor:
    def __init__(self, path, center_coordinates, scale_factor, rotation_speed, screen):
        self.path = path
        self.center_coordinates = center_coordinates
        self.scale_factor = scale_factor
        self.screen = screen

        self.icon = pygame.image.load(self.path).convert_alpha()
        self.icon_width = self.icon.get_size()[0]
        self.icon_height = self.icon.get_size()[1]
        self.final_size = (int(self.icon_width * self.scale_factor), int(self.icon_height * self.scale_factor))
        self.icon_final = pygame.transform.scale(self.icon, self.final_size)

        self.angle = randint(0, 179)
        self.rotation_speed = rotation_speed

    def draw(self):
        """ Draw the propeller with center-based mounting and delta time-based rotation. """
        # Rotate the image
        rotated_image = pygame.transform.rotate(self.icon_final, self.angle)

        # Get the rotated image's rect and center it at the given coordinates
        rect = rotated_image.get_rect(center=self.center_coordinates)
        self.screen.blit(rotated_image, rect)

        # Update the angle
        self.angle = (self.angle + self.rotation_speed * dt) % 360

class Drone:
    def __init__(self, obstacle_map, center_coordinates, orientation):
        self.sprite_path = "Mechatronics II/Drone Course Simulator/Assets/Drone_Disconnected_No_Prop.png"
        self.center_coordinates = (center_coordinates[0] + newX, center_coordinates[1])  # Now the center of the drone
        self.scale_factor = 2.5
        self.screen = main_screen
        self.obstacle_map = obstacle_map
        self.orientation = orientation
        self.speed_multipler = 1

        # Load and scale image
        self.icon = pygame.image.load(self.sprite_path).convert_alpha()
        self.icon_width, self.icon_height = self.icon.get_size()
        self.final_size = (int(self.icon_width * self.scale_factor), int(self.icon_height * self.scale_factor))
        self.icon_final = pygame.transform.scale(self.icon, self.final_size)

    def draw(self):
        """ Draw the drone centered on its coordinates """
        # Get the rect and position it based on the center
        rect = self.icon_final.get_rect(center=self.center_coordinates)
        self.screen.blit(self.icon_final, rect)

speed = 1600
prop1 = Propellor("Mechatronics II/Drone Course Simulator/Assets/Prop.png", (25 + newX, 100), 2.5, speed, main_screen)
prop2 = Propellor("Mechatronics II/Drone Course Simulator/Assets/Prop.png", (92.5 + newX, 100), 2.5, speed, main_screen)
prop3 = Propellor("Mechatronics II/Drone Course Simulator/Assets/Prop.png", (25 + newX, 175), 2.5, speed, main_screen)
prop4 = Propellor("Mechatronics II/Drone Course Simulator/Assets/Prop.png", (92.5 + newX, 175), 2.5, speed, main_screen)
drone_propellors = [prop1, prop2, prop3, prop4]
tello = Drone(None, (60, 135), None)

"""MAIN GAMELOOP"""
while running:  
    critical_events()
    main_screen_background()
    main_screen_menu()
    get_user_inputs()
    draw_obstacles()
    tello.draw()
    for prop in drone_propellors:
        prop.draw()
    

    if spup.execute:
        spup.draw()
        sbutton.draw()
        if sbutton.is_clicked():
            spup.execute = False
            spup2.execute = True
    
    elif spup2.execute:
        spup2.draw()
        sbutton2.draw()
        sbutton3.draw()
        if sbutton2.is_clicked():
            spup2.execute = False
            new_course_popup.execute = True

        elif sbutton3.is_clicked():
            spup2.execute = False
            edit_course_popup.execute = True
    
    elif new_course_popup.execute:
        new_course_popup.draw()
        new_course_finish_button.draw()
        text_box.draw(main_screen)

        if new_course_finish_button.is_clicked():
            text_box.submit = True

        elif text_box.submit:
            new_course_name = text_box.final_text
            new_course_popup.execute = False

            # Define the path manually
            filepath = f"Mechatronics II/Drone Course Simulator/Saved Maps/{new_course_name}.csv"

            # Create an empty CSV file
            with open(filepath, "w") as file:
                pass  # Just creates the file without writing anything`

            current_file = filepath
    
    elif edit_course_popup.execute:
        edit_course_popup.draw()
        edit_course_finish_button.draw()
        text_box_2.draw(main_screen)

        if edit_course_finish_button.is_clicked():
            text_box_2.submit = True

        elif text_box_2.submit:
            edit_course_name = f"{text_box_2.final_text}.csv"
            if edit_course_name not in all_files:
                text_box_2.submit = False
                text_box_2.text = ""
            else:
                current_file = f"Mechatronics II/Drone Course Simulator/Saved Maps/{edit_course_name}"

                process_file_load(current_file)

                edit_course_popup.execute = False


    elif save_options_popup.execute:
        save_options_popup.draw()
        save_button.draw()
        save_as_button.draw()
        
        if save_button.is_clicked():
            save_current_course()
            
    else:  
        for icon in menu_icons:
            if hitbox(icon.hitbox, mouse_hitbox):
                highlight_box = (icon.hitbox[0] - 2, icon.hitbox[1] - 2, icon.hitbox[2] + 4, icon.hitbox[3] + 4)
                pygame.draw.rect(main_screen, "white", highlight_box, 2)
                if not(moving or expanding):
                    if can_select and left_click:
                        icon.action()
                        can_select = False

        '''Calculating Shapes Physics'''
        obstacles = sorted(shape_blockchain_ids.values(), key = lambda x: x.layer, reverse = True)
        for shape in obstacles:
            """Calculate New Mouse layer"""
            if not (moving or altering_point_1 or altering_point_2 or altering_point_3 or expanding):
                if shape.type == 'arc' and (hitbox(shape.expansion_hitbox_1, mouse_hitbox) or hitbox(shape.expansion_hitbox_2, mouse_hitbox) or hitellipse(shape.expansion_hitbox_3, mouse_hitbox)):
                    if can_select and left_click:
                        mouse_layer = shape.layer
                        selected_blockchain_id = shape.blockchain_id
                        can_select = False

                if shape.type == 'ellipse' and (hitellipse(shape.hitbox, mouse_hitbox) or hitbox(shape.expansion_hitbox, mouse_hitbox)):
                    if can_select and left_click:
                        mouse_layer = shape.layer
                        selected_blockchain_id = shape.blockchain_id
                        can_select = False

                if shape.type == 'rectangle' and (hitbox(shape.hitbox, mouse_hitbox) or hitbox(shape.expansion_hitbox, mouse_hitbox)):
                    if can_select and left_click:
                        mouse_layer = shape.layer
                        selected_blockchain_id = shape.blockchain_id
                        can_select = False

            """Change Shape Sizes"""
            #Hehe later (needs to be run before center movements or the line object blows up due to necessary selection tolerance)
            if shape.type == 'arc':
                if (hitbox(shape.expansion_hitbox_1, mouse_hitbox) or altering_point_1) and not (moving or altering_point_2 or altering_point_3) and mouse_layer == shape.layer:
                    if left_click:
                        altering_point_1 = True
                        expanding = True
                        shape.x1 += change_x
                        shape.y1 += change_y
                        if not mouse_lock[0]:
                            mouse_lock = (True, shape, shape.x1, shape.y1, x_mouse, y_mouse)
                    else:
                        altering_point_1 = False
                        expanding = False
                        mouse_lock = (False, None, None, None, 0, 0)

                if (hitbox(shape.expansion_hitbox_2, mouse_hitbox) or altering_point_2) and not (moving or altering_point_1 or altering_point_3) and mouse_layer == shape.layer:
                    if left_click:
                        altering_point_2 = True
                        expanding = True
                        shape.x2 += change_x
                        shape.y2 += change_y

                        if not mouse_lock[0]:
                            mouse_lock = (True, shape, shape.x2, shape.y2, x_mouse, y_mouse)
                    else:
                        mouse_lock = (False, None, None, None, 0, 0)
                        altering_point_2 = False
                        expanding = False

                if (hitellipse(shape.expansion_hitbox_3, mouse_hitbox) or altering_point_3) and not (moving or altering_point_1 or altering_point_2) and mouse_layer == shape.layer:
                            if left_click:
                                shape.can_lock = False
                                shape_lock = False
                                altering_point_3 = True
                                expanding = True
                                shape.x3 += change_x
                                shape.y3 += change_y
                            
                            else:
                                shape.can_lock = True
                                mouse_lock = (False, None, None, None, 0, 0)
                                altering_point_3 = False
                                expanding = False

                if moving:
                    left_x = min(shape.expansion_hitbox_1[0], shape.expansion_hitbox_2[0])
                    top_y = min(shape.expansion_hitbox_1[1], shape.expansion_hitbox_2[1])
                    width = abs(shape.expansion_hitbox_1[0] - shape.expansion_hitbox_2[0]) + 20
                    height = abs(shape.expansion_hitbox_1[1] - shape.expansion_hitbox_2[1]) + 20
                    hit = hitborder((left_x, top_y, width, height))
                    if hit[2]:
                        shape.x += hit[0]
                        shape.y += hit[1]
                else:
                    hit_1 = hitborder(shape.expansion_hitbox_1)
                    hit_2 = hitborder(shape.expansion_hitbox_2)
                    hit_3 = hitborder(shape.expansion_hitbox_3)
                    if hit_1[2]:
                        shape.x1 += hit_1[0]
                        shape.y1 += hit_1[1]
                    if hit_2[2]:
                        shape.x2 += hit_2[0]
                        shape.y2 += hit_2[1]
                    if hit_3[2]:
                        shape.x3 += hit_3[0]
                        shape.y3 += hit_3[1]
                    
                    if snap_mode:
                        shape.x1, shape.y1 = snap_mode_correct(shape.x1, shape.y1)
                        shape.x2, shape.y2 = snap_mode_correct(shape.x2, shape.y2)

            else:
                if(hitbox(shape.expansion_hitbox, mouse_hitbox) or expanding) and not (moving or altering_point_1 or altering_point_2) and mouse_layer == shape.layer:
                    if left_click:
                        expanding = True
                        if shape.width > 20:
                            shape.width += change_x
                            shape.x += change_x / 2
                        elif shape.width == 20 and change_x > 0:
                            shape.x += change_x / 2
                            shape.width += change_x
                        else:
                            shape.width = 20
                        
                        if shape.height > 20:
                            shape.height -= change_y
                            shape.y += change_y / 2
                        elif shape.height == 20 and change_y < 0:
                            shape.y += change_y / 2
                            shape.height -= change_y
                        else:
                            shape.height = 20

                        if not mouse_lock[0]:
                            mouse_lock = (True, shape, shape.expansion_hitbox[0], shape.expansion_hitbox[1], x_mouse, y_mouse)
                    else:
                        shape_lock = (False, None, None)
                        mouse_lock = (False, None, None, None, 0, 0)
                        expanding = False
                
                if moving:
                    left_x = shape.hitbox[0]
                    top_y = shape.hitbox[1] - 20
                    width = shape.hitbox[2] + 20
                    height = shape.hitbox[3] + 20
                    hit = hitborder((left_x, top_y, width, height))
                    if hit[2]:
                        shape.x += hit[0]
                        shape.y += hit[1]
                else:
                    hit = hitborder(shape.expansion_hitbox)
                    if hit[2]:
                        shape.x += hit[0] / 2
                        shape.width += hit[0]
                        shape.y += hit[1] / 2
                        shape.height -= hit[1]
                    
                    if snap_mode:
                        result = snap_mode_correct(shape.expansion_hitbox[0], shape.expansion_hitbox[1])
                        shape.width += result[0] - shape.expansion_hitbox[0]
                        shape.x += (result[0] - shape.expansion_hitbox[0]) / 2
                        shape.height += result[1] - shape.expansion_hitbox[1]
                        shape.y += (result[1] - shape.expansion_hitbox[1]) / 2

            """Move Shape Centers"""
            if shape.type == 'arc' and shape.locked:
                if (hitline(shape.hitbox, mouse_hitbox) or moving) and not (altering_point_1 or altering_point_2 or expanding) and mouse_layer == shape.layer:
                    if left_click:
                        moving = True
                        shape.x1 += change_x
                        shape.x2 += change_x
                        shape.y1 += change_y
                        shape.y2 += change_y
                        if not mouse_lock[0]:
                            mouse_lock = (True, shape, shape.x, shape.y, x_mouse, y_mouse)
                    else:
                        mouse_lock = (False, None, None, None, 0, 0)
                        moving = False
            
            elif shape.type == "rectangle":
                if (hitbox(shape.hitbox, mouse_hitbox) or moving) and not (altering_point_1 or altering_point_2 or expanding) and mouse_layer == shape.layer:
                    if left_click:
                        moving = True
                        shape.x += change_x
                        shape.y += change_y
                        if not mouse_lock[0]:
                            mouse_lock = (True, shape, shape.x, shape.y, x_mouse, y_mouse)
                    else:
                        mouse_lock = (False, None, None, None, 0, 0)
                        moving = False

            elif shape.type == "ellipse":
                if(hitellipse(shape.hitbox, mouse_hitbox) or moving) and not (altering_point_1 or altering_point_2 or expanding) and mouse_layer == shape.layer:
                    if left_click:
                        moving = True
                        shape.x += change_x
                        shape.y += change_y
                        if not mouse_lock[0]:
                            mouse_lock = (True, shape, shape.x, shape.y, x_mouse, y_mouse)
                    else:
                        mouse_lock = (False, None, None, None, 0, 0)
                        moving = False

    gametime_runner()
    

"""FPS Check and Game Exit"""
print("Sim Exit")
print(f'Average FPS: {round(average_fps)}')
pygame.quit()