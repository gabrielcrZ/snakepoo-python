import pygame
import random
import sys
from pygame.math import Vector2
import os
pygame.init()

cell_size = 25
cell_number = 25
Dimension = cell_size * cell_number
window = pygame.display.set_mode((Dimension, Dimension))
pygame.display.set_caption("Snake")
FPS = 60

# Culori
verde_inchis = (0, 102, 0)
rosu = (255, 0, 0)
negru = (0, 0, 0)
verde_deschis = (0, 255, 26)


class BGROUND:
    def __init__(self):
        self.bground_image = pygame.image.load(os.path.join('p5 images', 'bground.jpg'))
        self.bground = pygame.transform.scale(self.bground_image, (Dimension, Dimension))

    def draw_background(self):
        window.blit(self.bground, (0, 0))


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            vect_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(window, negru, vect_rect)

    def move_snake(self):
        if self.new_block:
            copy = self.body[:]
            copy.insert(0, copy[0] + self.direction)
            self.body = copy[:]
            self.new_block = False
        else:
            copy = self.body[:-1]
            copy.insert(0, copy[0] + self.direction)
            self.body = copy[:]

    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        # pygame.draw.rect(window, rosu, fruit_rect)
        fruit_img = pygame.image.load(os.path.join('p5 images', 'Pear.png'))
        fruit = pygame.transform.scale(fruit_img, (cell_size, cell_size))
        window.blit(fruit, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.bground = BGROUND()
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.border_check()
        self.snake_fail()

    def draw(self):
        self.bground.draw_background()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.fruit.randomize()

    def border_check(self):
        if self.snake.body[0].x == -1:
            self.snake.body[0].x = cell_number
        if self.snake.body[0].x == cell_number+1:
            self.snake.body[0].x = 0
        if self.snake.body[0].y == -1:
            self.snake.body[0].y = cell_number
        if self.snake.body[0].y == cell_number+1:
            self.snake.body[0].y = 0

    def snake_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                pygame.quit()
                sys.exit()


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
main_game = MAIN()


clock = pygame.time.Clock()
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
    main_game.draw()
    pygame.display.update()
