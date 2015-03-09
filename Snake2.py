"""Softdes SP2015 Project 4 Interactive Programming, game design: NOKIA SNAKE"""
"""Authors: Hieu Nguyen and Ziyi Lan (Jason)"""

import pygame, copy, time, random
speed=10
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
        self.snake.add_part(0, round(random.randrange(30,width-30)/10.0)*10, round(random.randrange(30,height-30)/10.0)*10)
        self.apple = Apple(width, height)

    def update(self, apple):
        if self.snake.get_snake()[0]['x']==apple.x and self.snake.get_snake()[0]['y']==apple.y:
            apple.regenerate()
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

        return False

    def collided_with(self, snake2):
        body_parts_x1 = [self.snake.get_snake()[x]['x'] for x in range(1, self.part_number)]
        body_parts_y1 = [self.snake.get_snake()[y]['y'] for y in range(1, self.part_number)]

        head_x1 = self.snake.get_snake()[0]['x']
        head_y1 = self.snake.get_snake()[0]['y']

        body_parts_x2 = [snake2.snake.get_snake()[x]['x'] for x in range(1, snake2.part_number)]
        body_parts_y2 = [snake2.snake.get_snake()[y]['y'] for y in range(1, snake2.part_number)]

        head_x2 = snake2.snake.get_snake()[0]['x']
        head_y2 = snake2.snake.get_snake()[0]['y']

        for i in range(self.part_number):
            if head_x2 == self.snake.get_snake()[i]['x'] and head_y2 == self.snake.get_snake()[i]['y']:
                return True

        for i in range(snake2.part_number):
            if head_x1 == snake2.snake.get_snake()[i]['x'] and head_y1 == snake2.snake.get_snake()[i]['y']:
                return True

        return False


class AppleModel():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.apple = Apple(width, height)
        self.x = self.apple.x
        self.y = self.apple.y

    def regenerate(self):
        self.apple = Apple(self.width, self.height)
        self.x = self.apple.x
        self.y = self.apple.y


class SnakeView():

    def __init__(self, model1, model2, apple, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.model_1 = model1
        self.model_2 = model2
        self.apple = apple

    def draw(self):
        self.screen.fill(green) #Background color of the game.
        '''Drawing the border of the ground in which the snake will be moving'''
        self.screen.fill(black,rect=[0,10,800,10])
        self.screen.fill(black,rect=[0,580,800,10])
        self.screen.fill(black,rect=[10,0,10,600])
        self.screen.fill(black,rect=[780,0,10,600])

        #draws apple
        pygame.draw.rect(self.screen,red,[self.apple.x,self.apple.y,10,10])

        #draws head of snake
        pygame.draw.rect(self.screen,black,[self.model_1.snake.get_snake()[0]['x'], self.model_1.snake.get_snake()[0]['y'],10,10])
        pygame.draw.rect(self.screen,black,[self.model_2.snake.get_snake()[0]['x'], self.model_2.snake.get_snake()[0]['y'],10,10])

        #draws rest of snake
        for i in range(len(self.model_1.snake.get_snake())-1):
            pygame.draw.rect(self.screen,black,[self.model_1.snake.get_snake()[i+1]['x'], self.model_1.snake.get_snake()[i+1]['y'],10,10])

        for i in range(len(self.model_2.snake.get_snake())-1):
            pygame.draw.rect(self.screen,black,[self.model_2.snake.get_snake()[i+1]['x'], self.model_2.snake.get_snake()[i+1]['y'],10,10])

        pygame.display.update()
        
class SnakeController():
    def __init__(self, model1, model2):
        self.model_1 = model1
        self.model_2 = model2

    def process_events(self, snake1, snake2):
        for event in pygame.event.get():
            if pygame.key.get_focused():
                if pygame.key.get_pressed()[pygame.K_a]:
                    if snake1.get_snake()[0]['vel_x'] > 0:
                        pass
                    else:
                        snake1.get_snake()[0]['vel_x'] = -speed
                        snake1.get_snake()[0]['vel_y'] = 0

                elif pygame.key.get_pressed()[pygame.K_d]:
                    if snake1.get_snake()[0]['vel_x'] < 0:
                        pass
                    else:
                        snake1.get_snake()[0]['vel_x'] = speed
                        snake1.get_snake()[0]['vel_y'] = 0

                elif pygame.key.get_pressed()[pygame.K_w]:
                    if snake1.get_snake()[0]['vel_y'] > 0:
                        pass
                    else:
                        snake1.get_snake()[0]['vel_x']  = 0
                        snake1.get_snake()[0]['vel_y']  = -speed

                elif pygame.key.get_pressed()[pygame.K_s]:
                    if snake1.get_snake()[0]['vel_y'] < 0:
                        pass
                    else:
                        snake1.get_snake()[0]['vel_x'] = 0
                        snake1.get_snake()[0]['vel_y'] = speed


                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    if snake2.get_snake()[0]['vel_x'] > 0:
                        pass
                    else:
                        snake2.get_snake()[0]['vel_x'] = -speed
                        snake2.get_snake()[0]['vel_y'] = 0

                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    if snake2.get_snake()[0]['vel_x'] < 0:
                        pass
                    else:
                        snake2.get_snake()[0]['vel_x'] = speed
                        snake2.get_snake()[0]['vel_y'] = 0

                elif pygame.key.get_pressed()[pygame.K_UP]:
                    if snake2.get_snake()[0]['vel_y'] > 0:
                        pass
                    else:
                        snake2.get_snake()[0]['vel_x']  = 0
                        snake2.get_snake()[0]['vel_y']  = -speed

                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    if snake2.get_snake()[0]['vel_y'] < 0:
                        pass
                    else:
                        snake2.get_snake()[0]['vel_x'] = 0
                        snake2.get_snake()[0]['vel_y'] = speed


class Snake_Game():
    """ Main snake class """
    def __init__(self):
        self.model_1 = SnakeModel(800, 600)
        self.model_2 = SnakeModel(800, 600)
        self.apple = AppleModel(800, 600)
        self.view = SnakeView(self.model_1, self.model_2, self.apple, 800, 600)
        self.controller = SnakeController(self.model_1, self.model_2)

    def run(self):
        last_update_time = time.time()
        while not self.model_2.is_dead() and not self.model_1.is_dead() and not self.model_1.collided_with(self.model_2):
            self.view.draw()
            self.controller.process_events(self.model_1.snake, self.model_2.snake)
            self.model_1.update(self.apple)
            self.model_2.update(self.apple)
            clock.tick(FPS)
            last_update_time = time.time()


if __name__ == '__main__':
    snake = Snake_Game()
    snake.run()
