"""Softdes SP2015 Project 4 Interactive Programming, game design: NOKIA SNAKE"""
"""Authors: Hieu Nguyen and Ziyi Lan (Jason)"""

import pygame, copy, time, random

#pygame.init()

speed = 10

white=(255,255,255)
black=(0,0,0)
green=(170,249,186)
red = (255,0,0)

clock=pygame.time.Clock()
FPS=20

class Snake_part():
    def __init__(self, k, x, y): #k is kth part of the body
        self.x = x
        self.y = y
        self.number = k
        self.info = {}

    def get_info(self, k, snake):
        if not snake: #if snake is empty i.e. if part is head
            return {'x': self.x, 'y': self.y, 'vel_x': speed, 'vel_y': 0}
        else:
            tail = snake[k-1]
            self.info['vel_x'] = tail['vel_x']
            self.info['vel_y'] = tail['vel_y']

            if tail['vel_x'] > 0:
                self.info['x'] = tail['x'] - speed
                self.info['y'] = tail['y']
            elif tail['vel_x'] < 0:
                self.info['x'] = tail['x'] + speed
                self.info['y'] = tail['y']
            elif tail['vel_y'] > 0:
                self.info['x'] = tail['x']
                self.info['y'] = tail['y'] - speed
            elif tail['vel_y'] < 0:
                self.info['x'] = tail['x']
                self.info['y'] = tail['y'] + speed

            return self.info


class Snake():
    def __init__(self):
        self.snake = {}

    def add_part(self, k, x=0, y=0):
        part = Snake_part(k, x, y)
        self.snake[k] = part.get_info(k, self.snake)

    def get_snake(self):
        return self.snake

    def update_snake(self):
        for i in range(len(self.snake)-1, 0, -1):
            self.snake[i] = copy.deepcopy(self.snake[i-1])

        head = self.snake[0]
        head['x'] = round(head['x'] + head['vel_x'])
        head['y'] = round(head['y'] + head['vel_y'])


class Display():
    def __init__(self,xspan,yspan,caption):
        self.xspan = xspan
        self.yspan = yspan
        self.caption = caption


class Apple():
    def __init__(self,xspan,yspan):
        self.x = round(random.randrange(30,xspan-30)/10.0)*10
        self.y = round(random.randrange(30,yspan-30)/10.0)*10

        
class SnakeModel():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.part_number = 0
        self.background = Display(width, height, 'Snake Game')
        self.snake = Snake()
        self.snake.add_part(0, 200, 40)
        self.apple = Apple(width, height)

    def update(self):
        if self.snake.get_snake()[0]['x']==self.apple.x and self.snake.get_snake()[0]['y']==self.apple.y:
            self.apple = Apple(self.width, self.height)
            for i in range(2):
                self.part_number += 1
                self.snake.add_part(self.part_number)
        self.snake.update_snake()

    def is_dead(self):
        #tests if snake hits borders
        if self.snake.get_snake()[0]['x']<20 or self.snake.get_snake()[0]['x']>770 or \
                self.snake.get_snake()[0]['y']<20 or self.snake.get_snake()[0]['y']>570:
            return True

        #tests if snake hits itself:
        body_parts_x = [self.snake.get_snake()[x]['x'] for x in range(1, self.part_number)]
        body_parts_y = [self.snake.get_snake()[y]['y'] for y in range(1, self.part_number)]

        head_x = self.snake.get_snake()[0]['x']
        head_y = self.snake.get_snake()[0]['y']

        for i in range(1, self.part_number):
            if head_x == self.snake.get_snake()[i]['x'] and head_y == self.snake.get_snake()[i]['y']:
                return True


class SnakeView():
    def __init__(self, model, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.model = model

    def draw(self):
        self.screen.fill(green) #Background color of the game.
        '''Drawing the border of the ground in which the snake will be moving'''
        self.screen.fill(black,rect=[0,10,800,10])
        self.screen.fill(black,rect=[0,580,800,10])
        self.screen.fill(black,rect=[10,0,10,600])
        self.screen.fill(black,rect=[780,0,10,600])

        #draws apple
        pygame.draw.rect(self.screen,red,[self.model.apple.x,self.model.apple.y,10,10])

        #draws head of snake
        pygame.draw.rect(self.screen,black,[self.model.snake.get_snake()[0]['x'], self.model.snake.get_snake()[0]['y'],10,10])

        #draws rest of snake
        for i in range(len(self.model.snake.get_snake())-1):
            pygame.draw.rect(self.screen,black,[self.model.snake.get_snake()[i+1]['x'], self.model.snake.get_snake()[i+1]['y'],10,10])

        pygame.display.update()
        
        
class SnakeController():
    def __init__(self, model):
        self.model = model

    def process_events(self, snake):
        for event in pygame.event.get():
            if pygame.key.get_focused():
                if pygame.key.get_pressed()[pygame.K_a]:
                    if snake.get_snake()[0]['vel_x'] > 0:
                        pass
                    else:
                        snake.get_snake()[0]['vel_x'] = -speed
                        snake.get_snake()[0]['vel_y'] = 0

                elif pygame.key.get_pressed()[pygame.K_d]:
                    if snake.get_snake()[0]['vel_x'] < 0:
                        pass
                    else:
                        snake.get_snake()[0]['vel_x'] = speed
                        snake.get_snake()[0]['vel_y'] = 0

                elif pygame.key.get_pressed()[pygame.K_w]:
                    if snake.get_snake()[0]['vel_y'] > 0:
                        pass
                    else:
                        snake.get_snake()[0]['vel_x']  = 0
                        snake.get_snake()[0]['vel_y']  = -speed

                elif pygame.key.get_pressed()[pygame.K_s]:
                    if snake.get_snake()[0]['vel_y'] < 0:
                        pass
                    else:
                        snake.get_snake()[0]['vel_x'] = 0
                        snake.get_snake()[0]['vel_y'] = speed


class Snake_Game():
    """ Main snake class """

    def __init__(self):
        self.model = SnakeModel(800, 600)
        self.view = SnakeView(self.model, 800, 600)
        self.controller = SnakeController(self.model)

    def run(self):
        last_update_time = time.time()
        while not (self.model.is_dead()):
            self.view.draw()
            self.controller.process_events(self.model.snake)
            self.model.update()
            clock.tick(FPS)
            last_update_time = time.time()


if __name__ == '__main__':
    snake = Snake_Game()
    snake.run()