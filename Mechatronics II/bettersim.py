'''Libraries'''
import pygame
import math
pygame.init()

'''Shape Classes'''
class line_object(object):
    def __init__(self, id, x1, y1, x2, y2, color, layer, surface):
        self.id = id
        self.type = 'line'
        self.layer = layer
        self.x = 0
        self.y = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.surface = surface
        self.hitbox = (x1, y1, x2, y2)
        self.expansion_hitbox_1 = (x1 - 20, y1 - 20, 20, 20)
        self.expansion_hitbox_2 = (x2 - 20, y2 - 20, 20, 20)

    def draw(self):
        pygame.draw.line(self.surface, self.color, (self.x1 + self.x, self.y1+ self.y), (self.x2 + self.x, self.y2 + self.y), 5)
        self.hitbox = (self.x1 + self.x, self.y1 + self.y, self.x2 + self.x, self.y2 + self.y)
        self.expansion_hitbox_1 = (self.x1 + self.x - 10, self.y1 + self.y - 10, 20, 20)
        self.expansion_hitbox_2 = (self.x2 + self.x - 10, self.y2 + self.y - 10, 20, 20)
        pygame.draw.rect(self.surface, "blue", self.expansion_hitbox_1, 2)
        pygame.draw.rect(self.surface, "blue", self.expansion_hitbox_2, 2)

class ellipse_object(object):
    def __init__(self, id, x, y, width, height, color, layer, surface):
        self.id = id
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
        pygame.draw.rect(self.surface, "blue", self.expansion_hitbox, 2)

class rectangle_object(object):
    def __init__(self, id, x, y, width, height, color, layer, surface):
        self.id = id
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
        pygame.draw.rect(self.surface, "blue", self.expansion_hitbox, 2)

class drone(object):
    pass

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
    elif right_x > screen_size_x: x = screen_size_x - right_x
    if top_y < 0: y = -top_y
    elif bottom_y > screen_size_y: y = screen_size_y - bottom_y
    
    if y != 0 or x != 0:
        hit = True
    changes = (x, y, hit)
    return(changes)

def mousecorrect(locked, shape, center_x, center_y, relative_x, relative_y):
    if not locked:
        return
    global x_mouse
    global y_mouse
    
    delta_x = relative_x - center_x
    delta_y = relative_y - center_y

    if shape.type == "line":
        if altering_point_1:
            set_x = shape.x1
            set_y = shape.y1
        elif altering_point_2:
            set_x = shape.x2
            set_y = shape.y2
        else:
            set_x = shape.x
            set_y = shape.y
    
    else:
        if expanding:
            set_x = shape.expansion_hitbox[0]
            set_y = shape.expansion_hitbox[1]
        else:
            set_x = shape.x
            set_y = shape.y

    if x_mouse != set_x + delta_x or y_mouse != set_y + delta_y:
        x_mouse = set_x + delta_x
        y_mouse = set_y + delta_y
        pygame.mouse.set_pos(x_mouse, y_mouse)



'''Start Variables'''
#Screen starting constants
screen_size_x = 750
screen_size_y = 750
screen = pygame.display.set_mode((screen_size_x, screen_size_y), pygame.RESIZABLE)
background_color = (74, 109, 229)
accent_color = (206, 176, 247)
menu_width = 100
tab_height = 75
newX = menu_width + 1

#Gametime starting constants
running = True
dt = 0
clock = pygame.time.Clock()
times_averaged = 0
average_fps = 0

#Inputs starting constants
pygame.mouse.set_cursor(pygame.cursors.arrow)
hit = False
mouse_lock = (False, None, None, None, 0, 0)#locked, object, mouse_x, mouse_y
print(mouse_lock[0])
x_mouse = screen_size_x / 2
y_mouse = screen_size_y / 2
pygame.mouse.set_pos(x_mouse, y_mouse)
mouse_layer = 1
snap_mode = False

#Objects starting constants
shape_lock = (False, None, None)
shape_objects = []
moving = False
altering_point_1 = False
altering_point_2 = False
expanding = False
can_select = True
select_countdown = 0

'''Test Objects'''
line_1 = line_object(0, 50 + newX, 50, 100 + newX, 100, "yellow", 1, screen)
shape_objects.append(line_1)
line_2 = line_object(1, 200 + newX, 200, 500, 500, "red", 2, screen)
shape_objects.append(line_2)
rectangle_1 = rectangle_object(2, 200, 350, 35, 48, "orange", 3, screen)
shape_objects.append(rectangle_1)
ellipse_1 = ellipse_object(3, 500, 500, 100, 50, "green", 4, screen)
shape_objects.append(ellipse_1)


"""MAIN GAMELOOP"""
while running:
    '''Critical Events'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWRESIZED:
            screen_size_x, screen_size_y = pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]

    '''Background and Grid lines'''
    screen.fill(background_color)
    for i in range(newX + 20, screen_size_x + 1, 20):
        pygame.draw.line(screen, accent_color, (i, 0), (i, screen_size_y))
    for i in range(0, screen_size_y + 1, 20):
        pygame.draw.line(screen, accent_color, (newX, i), (screen_size_x, i))

    '''Menu'''
    pygame.draw.rect(screen, "black", (0, 0, menu_width, screen_size_y))
    for i in range(9):
        pygame.draw.line(screen, "white", (0, i * tab_height), (menu_width, i * tab_height))
    pygame.draw.line(screen, "white", (menu_width, 0), (menu_width, screen_size_y))

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

    '''Drawing Shapes'''
    for shape in shape_objects:
        shape.draw()
    '''Calculating Shapes Physics'''
    shapes_physics = sorted(shape_objects, key = lambda x: x.layer, reverse = True)
    for shape in shapes_physics:
        """Calculate New Mouse layer"""
        if not (moving or altering_point_1 or altering_point_2 or expanding):
            if shape.type == 'line' and (hitline(shape.hitbox, mouse_hitbox) or hitbox(shape.expansion_hitbox_1, mouse_hitbox) or hitbox(shape.expansion_hitbox_1, mouse_hitbox)):
                if can_select and left_click:
                    mouse_layer = shape.layer
                    can_select = False
            
            if shape.type == 'ellipse' and (hitellipse(shape.hitbox, mouse_hitbox) or hitbox(shape.expansion_hitbox, mouse_hitbox)):
                if can_select and left_click:
                    mouse_layer = shape.layer
                    can_select = False

            if shape.type == 'rectangle' and (hitbox(shape.hitbox, mouse_hitbox) or hitbox(shape.expansion_hitbox, mouse_hitbox)):
                if can_select and left_click:
                    mouse_layer = shape.layer
                    can_select = False

            if not can_select:
                select_countdown += dt
            if select_countdown >= 0.5:
                select_countdown = 0
                can_select = True

        """Change Shape Sizes"""
        #Hehe later (needs to be run before center movements or the line object blows up due to necessary selection tolerance)
        if shape.type == 'line':
            if (hitbox(shape.expansion_hitbox_1, mouse_hitbox) or altering_point_1) and not (moving or altering_point_2) and mouse_layer == shape.layer:
                if left_click:
                    altering_point_1 = True
                    expanding = True
                    '''right_x = shape.expansion_hitbox_1[0] + shape.expansion_hitbox_1[2]
                    left_x = shape.expansion_hitbox_1[0]
                    if right_x < screen_size_x and left_x > newX:
                        shape.x1 += change_x
                    elif right_x >= screen_size_x:
                        shape.x1 = screen_size_x - 1
                    shape.y1 += change_y'''


                    shape.x1 += change_x
                    shape.y1 += change_y
                    if not mouse_lock[0]:
                        mouse_lock = (True, shape, shape.x1, shape.y1, x_mouse, y_mouse)
                else:
                    altering_point_1 = False
                    expanding = False
                    mouse_lock = (False, None, None, None, 0, 0)

                

            if (hitbox(shape.expansion_hitbox_2, mouse_hitbox) or altering_point_2) and not (moving or altering_point_1) and mouse_layer == shape.layer:
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
                if hit_1[2]:
                    print(shape.expansion_hitbox_1)
                    shape.x1 += hit_1[0]
                    shape.y1 += hit_1[1]
                if hit_2[2]:
                    shape.x2 += hit_2[0]
                    shape.y2 += hit_2[1]
    
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

                    if shape_lock[0]:
                        if shape.hitbox[0] != shape_lock[1] or shape.hitbox[1] + shape.hitbox[3] != shape_lock[2]:
                            print("HORPFLANFO")
                            print(shape_lock, shape.hitbox[0], shape.hitbox[1] + shape.hitbox[3])
                            shape.x += shape_lock[1] - shape.hitbox[0]
                            shape.y += shape_lock[2] - (shape.hitbox[1] + shape.hitbox[3])


                    if not shape_lock[0]:
                        shape_lock = (True, shape.hitbox[0], shape.hitbox[1] + shape.hitbox[3])

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
                hit = hitborder(left_x, top_y, width, height)
            else:
                pass

        """Move Shape Centers"""
        if shape.type == 'line':
            if (hitline(shape.hitbox, mouse_hitbox) or moving) and not (altering_point_1 or altering_point_2 or expanding) and mouse_layer == shape.layer:
                if left_click:
                    moving = True
                    shape.x += change_x
                    shape.y += change_y
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

    #mousecorrect(mouse_lock[0], mouse_lock[1], mouse_lock[2], mouse_lock[3], mouse_lock[4], mouse_lock[5])

    '''Gametime Runner'''
    pygame.display.flip()
    dt = clock.tick() / 1000
    times_averaged += 1
    if times_averaged == 0:
        average_fps = clock.get_fps()
    else:
        average_fps += (clock.get_fps() - average_fps) / times_averaged
    

"""FPS Check and Game Exit"""
print("Sim Exit")
print(f'Average FPS: {round(average_fps)}')
pygame.quit()