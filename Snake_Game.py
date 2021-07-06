import pygame 
import time
import random

pygame.init()

class Cube:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def move(self, x_move, y_move):
        self.x += x_move
        self.y += y_move
    
    def redraw(self, surface, border=False, border_color=None):
        self.cube = pygame.draw.rect(surface, self.color, (self.x, self.y, 25, 25))
        if border == True:
            pygame.draw.rect(surface, border_color, (self.x, self.y, 25, 25), 3)

class Snake:
    def __init__(self, x, y, head_color,color, len=3,border=False, border_color=None):
        self.x = x
        self.y = y
        self.head_color = head_color
        self.color = color
        self.len = len
        self.is_alive = True
        self.border = border
        self.border_color = border_color

        self.create()
        for i in range(self.len):
            self.update()

    def create(self):
        self.head = Cube(self.x, self.y, self.head_color)
        self.body = [Cube(self.x, self.y, self.color) for i in range(self.len)]
        self.head_dir = [1, 0]
        self.body_loc = [[self.head.x, self.head.y] for i in range(self.len)]

    def check_collision(self):
        for i in range(1, self.len):
            if self.head.x == self.body[i].x and self.head.y == self.body[i].y:
                return False
        return True

    def move(self, dirc):
        self.head_dir = dirc

    def draw(self, surface):
        for i in range(self.len):
            self.body[i].redraw(surface, self.border, self.border_color)
            self.head.redraw(surface)

    def update(self):
        self.is_alive = self.check_collision()
        self.head.move(self.head_dir[0]*25, self.head_dir[1]*25)
        self.body_loc = [[self.head.x, self.head.y]] + self.body_loc[:-1]
        for i in range(self.len):
            self.body[i].x = self.body_loc[i][0]
            self.body[i].y = self.body_loc[i][1]

        if self.head.x < 0 or self.head.x == 500:
            self.is_alive = False

        elif self.head.y < 0 or self.head.y == 500:
            self.is_alive = False
            
    def inc_len(self):
        self.len += 1
        self.body_loc = [[self.head.x, self.head.y]] + self.body_loc
        self.body.append(Cube(self.body_loc[-1][0], self.body_loc[-1][1], self.color))

class Apple:
    def __init__(self, color, border=False, border_color=None):
        self.color = color
        self.border = border
        self.border_color = border_color
        self.x = 0
        self.y = 0
        self.cube = Cube(self.x, self.y, self.color)

    def generate(self):
        self.cube.x = random.randrange(0, 500/25)*25
        self.cube.y = random.randrange(0, 500/25)*25
        self.x = self.cube.x
        self.y = self.cube.y

    def draw(self, surface):
        self.cube.redraw(surface, self.border, self.border_color)

RED = (255, 0, 0)
DARK_RED = (125, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 125, 0)
LIGHT_DARK_GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
speed = 1/10
title = "Snake Game"

surface = pygame.display.set_mode((500, 500))
pygame.display.set_caption(title)
clock = pygame.time.Clock()
snake = Snake(150, 150, LIGHT_DARK_GREEN,GREEN, border=True, border_color=DARK_GREEN)
apple = Apple(RED, True ,DARK_RED)
apple.generate()
score_value = 0
font_small = pygame.font.SysFont('Arial',16)
gameLoop = True
t = time.time()

while gameLoop == True:
    clock.tick(FPS)

    if round(time.time()-t, 3) > speed and snake.is_alive:
        snake.update()
        t = time.time()
    
    if (apple.x == snake.head.x) and (apple.y == snake.head.y):
        apple.generate()
        score_value += 1
        snake.inc_len()

    if snake.is_alive == False:
        pass

    score_label = font_small.render(f"Score : {str(score_value)}", True, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.KEYDOWN and snake.is_alive:
            if event.key == pygame.K_UP and snake.head_dir != [0, 1]:
                snake.move([0, -1])
            elif event.key == pygame.K_DOWN and snake.head_dir != [0, -1]:
                snake.move([0, 1])
            elif event.key == pygame.K_LEFT and snake.head_dir != [1, 0]:
                snake.move([-1, 0])
            elif event.key == pygame.K_RIGHT and snake.head_dir != [-1, 0]:
                snake.move([1, 0])

    surface.fill(WHITE)
    snake.draw(surface)
    apple.draw(surface)
    surface.blit(score_label, (10, 10))
    pygame.display.flip()

pygame.quit()
quit()