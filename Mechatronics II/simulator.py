import math, pygame, sys
pygame.init()

class line_object(object):
    def __init__(self, x1, y1, x2, y2, color, layer, surface):
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
    def __init__(self, x, y, x_length, y_length, color, layer, surface):
        self.type = 'ellipse'
        self.layer = layer
        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length
        self.color = color
        self.surface = surface
        self.hitbox = (x, y, x_length, y_length)
        self.expansion_hitbox = (x + x_length / 2, y - y_length / 2 - 20, 20, 20)

    def draw(self):
        pygame.draw.ellipse(self.surface, self.color, (self.x - self.x_length / 2, self.y - self.y_length / 2, self.x_length, self.y_length))
        self.hitbox = (self.x, self.y, self.x_length, self.y_length)
        self.expansion_hitbox = (self.x + self.x_length / 2, self.y - self.y_length / 2 - 20, 20, 20)
        pygame.draw.rect(self.surface, "blue", self.expansion_hitbox, 2)

class square_object(object):
    def __init__(self, x, y, x_length, y_length, color, layer, surface):
        self.type = 'square'
        self.layer = layer
        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length
        self.color = color
        self.surface = surface
        self.hitbox = (x - x_length / 2, y - y_length / 2, x_length, y_length)
        self.expansion_hitbox = (x + x_length / 2, y - y_length / 2 - 20, 20, 20)
    
    def draw(self):
        self.hitbox = (self.x - self.x_length / 2, self.y - self.y_length / 2, self.x_length, self.y_length)
        self.expansion_hitbox = (self.x + self.x_length / 2, self.y - self.y_length / 2 - 20, 20, 20)
        pygame.draw.rect(self.surface, self.color, self.hitbox)
        pygame.draw.rect(self.surface, "blue", self.expansion_hitbox, 2)

class arc(object):
    def __init__(self, x1, y1, x2, y2):
        print()

def hitbox_check(hitbox_stationary, type, hitbox_mobile):
    if type == 'square':
        if hitbox_mobile[0] >= hitbox_stationary[0] and hitbox_mobile[0] + hitbox_mobile[2] <= hitbox_stationary[0] + hitbox_stationary[2]:
            if hitbox_mobile[1] >= hitbox_stationary[1] and hitbox_mobile[1] + hitbox_mobile[3] <= hitbox_stationary[1] + hitbox_stationary[3]:
                return True
        return False
    
    if type == 'ellipse':
        if ((((hitbox_mobile[0] - hitbox_stationary[0])) ** 2 / ((hitbox_stationary[2] / 2) ** 2)) + (((hitbox_mobile[1] - hitbox_stationary[1]) ** 2) / ((hitbox_stationary[3] / 2) ** 2))) <= 1:
            return True
        return False
    
    if type == 'line':
        try:
            slope = (hitbox_stationary[1]- hitbox_stationary[3]) / (hitbox_stationary[0] - hitbox_stationary[2])
            b = hitbox_stationary[1] - (slope * hitbox_stationary[0])
            if hitbox_stationary[0] > hitbox_stationary [2]:
                greater = hitbox_stationary[0]
                lesser = hitbox_stationary[2]
            else:
                greater = hitbox_stationary[2]
                lesser = hitbox_stationary[0]
            if (abs(hitbox_mobile[1] - (slope * hitbox_mobile[0] + b)) <= abs(8 * (1 + abs(slope)))) and (lesser <= hitbox_mobile[0] <= greater):
                return True
        except ZeroDivisionError:
            if abs(hitbox_mobile[0] - hitbox_stationary[0]) <= 8:
                return True
        return False
    
def overmove_correct(shape, check):
    if check == 'body':
        if shape.type == 'square':
            if (shape.hitbox[0] % (20 + (screen_size_x * 0.1))) > 10:
                shape.x += (20 - shape.hitbox[0] % 20)
            elif (shape.hitbox[0] % (20 + (screen_size_x * 0.1))) <= 10:
                shape.x -= (shape.hitbox[0] % 20)

            if ((shape.hitbox[1] + shape.hitbox[3]) % 20) > 10:
                shape.y += 20 - (shape.hitbox[1] + shape.hitbox[3]) % 20
            elif ((shape.hitbox[1] + shape.hitbox[3]) % 20) <= 10:
                shape.y -= (shape.hitbox[1] + shape.hitbox[3]) % 20
        
        if shape.type == 'ellipse':
            if ((shape.hitbox[0] - shape.hitbox[2] / 2) % 20) > 10:
                shape.x += 20 - (shape.hitbox[0] - shape.hitbox[2] / 2) % 20
            elif ((shape.hitbox[0] - shape.hitbox[2] / 2) % 20) <= 10:
                shape.x -= (shape.hitbox[0] - shape.hitbox[2] / 2) % 20

            if ((shape.hitbox[1] + shape.hitbox[3] / 2) % 20) > 10:
                shape.y += 20 - (shape.hitbox[1] + shape.hitbox[3] / 2) % 20
            elif ((shape.hitbox[1] + shape.hitbox[3] / 2) % 20) <= 10:
                shape.y -= (shape.hitbox[1] + shape.hitbox[3] / 2) % 20

    if check == 'expander':
        if shape.type != 'line':
            if (shape.expansion_hitbox[0] % 20) > 10:
                shape.x_length += 20 - shape.expansion_hitbox[0] % 20
                shape.x += (20 - shape.expansion_hitbox[0] % 20) / 2
            elif (shape.expansion_hitbox[0] % 20) <= 10:
                shape.x_length -= shape.expansion_hitbox[0] % 20
                shape.x -= (shape.expansion_hitbox[0] % 20) / 2
            
            if ((shape.expansion_hitbox[1] + 20) % 20) > 10:
                shape.y_length -= 20 - (((shape.expansion_hitbox[1] + 20) % 20))
                shape.y += (20 - ((shape.expansion_hitbox[1] + 20) % 20)) / 2
            elif ((shape.expansion_hitbox[1] + 20) % 20) <= 10:
                shape.y_length += ((shape.expansion_hitbox[1] + 20) % 20)
                shape.y -= ((shape.expansion_hitbox[1] + 20) % 20) / 2

screen_size_x, screen_size_y = 500, 500
screen = pygame.display.set_mode((screen_size_x, screen_size_y), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0
pygame.mouse.set_cursor(*pygame.cursors.arrow)
old_x, old_y, mouse_layer = screen.get_width() / 2, screen.get_height() / 2, 5

shapes = []
first = ellipse_object(500, 500, 60, 60, "green", 1, screen)
second = ellipse_object(600, 600, 20, 20, "red", 2, screen)
shapes.append(first)
shapes.append(second)
third = square_object(100, 100, 40, 40, "yellow", 3, screen)
shapes.append(third)
fourth = line_object(40, 40, 70, 70, "orange", 4, screen)
shapes.append(fourth)
fifth = ellipse_object(70, 60, 100, 40, "blue", 5, screen)
shapes.append(fifth)

expanding, moving = False, False
altering_1, altering_2 = False, False
clickable, count, windowcount, usable = True, 0, 0, True
fps = 0
background_color = (12, 56, 125)
accent_color = (7, 44, 102)
snap_mode = False
counter_x, counter_y = 0, 0
fps_count = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.WINDOWRESIZED:
            screen_size_x, screen_size_y = pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]

    screen.fill(background_color)

    pygame.draw.rect(screen, "black", (0, 0, (screen_size_x * 0.1), screen_size_y))
    pygame.draw.line(screen, "white", ((screen_size_x * 0.1), 0), ((screen_size_x * 0.1), screen_size_y))
    for i in range(0, int(5 * (screen_size_y * 0.1) + 1), int(screen_size_y * 0.1)):
        pygame.draw.line(screen, "white", (0, i), ((screen_size_x * 0.1), i))

    for i in range(int(screen_size_x * 0.1) + 20, screen_size_x + 1, 20):
        pygame.draw.line(screen, accent_color, (i, 0), (i, screen_size_y), 2)
    
    for i in range(0, screen_size_y + 1, 20):
        pygame.draw.line(screen, accent_color, (screen_size_x * 0.1 + 1, i), (screen_size_x, i), 2)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        running = False

    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        snap_mode = True
    else:
        snap_mode = False

    x_mouse, y_mouse = pygame.mouse.get_pos()
    mouse_hitbox = (x_mouse, y_mouse, 1, 1)
    left_click = list(pygame.mouse.get_pressed())[0]
    change_x, change_y = x_mouse - old_x, y_mouse - old_y

    if snap_mode:
        counter_x += x_mouse - old_x
        if abs(counter_x) < 20:
            change_x = 0
        else:
            change_x = counter_x
            counter_x = 0

        counter_y += y_mouse - old_y
        if abs(counter_y) < 20:
            change_y = 0
        else:
            change_y = counter_y
            counter_y = 0

    old_x, old_y = x_mouse, y_mouse

    for shape in shapes:
        shape.draw()

    shapes_physics = sorted(shapes, key = lambda x: x.layer, reverse = True)
    for shape in shapes_physics:
        
        if shape.type == 'line':
            if (hitbox_check(shape.expansion_hitbox_1, 'square', mouse_hitbox) or altering_1) and not moving and not altering_2 and mouse_layer == shape.layer:
                if left_click:
                    expanding = True
                    altering_1 = True
                    shape.x1 += change_x
                    shape.y1 += change_y
                    overmove_correct(shape, "expander")
                else:
                    altering_1, expanding = False, False
            
            if (hitbox_check(shape.expansion_hitbox_2, 'square', mouse_hitbox) or altering_2) and not moving and not altering_1 and mouse_layer == shape.layer:
                if left_click:
                    expanding = True
                    altering_2 = True
                    shape.x2 += change_x
                    shape.y2 += change_y
                    overmove_correct(shape, "expander")
                else:
                    altering_2, expanding = False, False

        else:
            if (hitbox_check(shape.expansion_hitbox, 'square', mouse_hitbox) or expanding) and not moving and mouse_layer == shape.layer: # Growth box check
                if left_click:
                    expanding = True
                    if shape.x_length == 20:
                        if change_x > 0:
                            shape.x_length += change_x
                            shape.x += change_x / 2  
                    elif shape.x_length < 20:
                        shape.x_length = 20
                    else:
                        shape.x_length += change_x
                        shape.x += change_x / 2
                    
                    if shape.y_length == 20:
                        if change_y < 0:
                            shape.y_length -= change_y
                            shape.y += change_y / 2
                    elif shape.y_length < 20:
                        shape.y_length = 20
                    else:
                        shape.y_length -= change_y
                        shape.y += change_y / 2
                    if snap_mode:
                        overmove_correct(shape, "expander")
                else:
                    expanding = False

        if (hitbox_check(shape.hitbox, shape.type, mouse_hitbox) or moving) and not expanding and mouse_layer == shape.layer:
            if left_click:
                    moving = True
                    shape.x += change_x
                    shape.y += change_y
                    if snap_mode:
                        overmove_correct(shape, "body")
            else:
                moving = False

        if shape.type == 'line':
            if not moving and not expanding and (hitbox_check(shape.hitbox, shape.type, mouse_hitbox) or hitbox_check(shape.expansion_hitbox_1, 'square', mouse_hitbox) or hitbox_check(shape.expansion_hitbox_2, 'square', mouse_hitbox)):
                if left_click and clickable:
                    mouse_layer = shape.layer
                    clickable = False
                count += dt
                if count > 0.25:
                    count = 0
                    clickable = True
        else:
            if not moving and not expanding and (hitbox_check(shape.hitbox, shape.type, mouse_hitbox) or hitbox_check(shape.expansion_hitbox, 'square', mouse_hitbox)):
                if left_click and clickable:
                    mouse_layer = shape.layer
                    clickable = False
                count += dt
                if count > 0.25:
                    count = 0
                    clickable = True
                    
    pygame.display.flip()

    dt = clock.tick() / 1000
    fps_count.append(clock.get_fps())
    fps = (fps + clock.get_fps()) / 2

print(fps)
print(sys.getsizeof(fps_count))
fps = 0
for item in fps_count:
    fps += item
fps = fps / len(fps_count)
print(fps)
pygame.quit()