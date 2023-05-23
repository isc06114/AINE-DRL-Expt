import os
import random
import sys
import time

import numpy as np
import pygame


class Setting:
    # ----- [ Window Position ] -----
    win_posx = 700
    win_posy = 300
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)

    # ----- [ Window Size ] -----

    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 1280
    GRID = 20
    GRID_WIDTH = int(WINDOW_WIDTH/GRID)
    GRID_HEIGHT = int(WINDOW_HEIGHT/GRID)

    # ----- [ Color ] -----

    BLACK = 0, 0, 0
    WHITE = 255,255,255
    RED = 255, 0, 0
    BLUE = 0, 0, 255

    AI = 0, 70, 255
    PLAYER = 25, 255, 25
    BODY = 233, 249, 185


    DARK_GRAY = 20, 20, 20
    LIGHT_GRAY = 80, 80, 80
    # ----- [Driection] -----  
    NORTH = ( 0, -1)
    SOUTH = ( 0,  1)
    WEST  = (-1,  0)
    EAST  = ( 1,  0)

    def get_direction(self, discrete):
        if discrete == 0:
            return self.NORTH
        if discrete == 1:
            return self.SOUTH
        if discrete == 2:
            return self.WEST
        return self.EAST
    # ===== [Print Image and Array] =====      
    def UpdateMap(self,screen):
        r_image = screen
        #pygame.image.save(r_image, "mapping.png")
        return pygame.surfarray.array3d(r_image)


    def draw_background(self,surface):
        background = pygame.Rect((0,0),(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.draw.rect(surface, self.WHITE, background)
        self.draw_grid(surface)

    def draw_grid(self,surface):
        for row in range(0,int(self.GRID_HEIGHT)):
            for col in range(0, int(self.GRID_WIDTH)):
                if (row+col) % 2 == 0:
                    rect = pygame.Rect((col*self.GRID, row*self.GRID), (self.GRID, self.GRID))
                    pygame.draw.rect(surface, self.DARK_GRAY, rect)
                else:
                    rect = pygame.Rect((col*self.GRID, row*self.GRID), (self.GRID, self.GRID))
                    pygame.draw.rect(surface, self.LIGHT_GRAY, rect)


    def draw_object(self,surface, color, pos):
        rect = pygame.Rect((pos[0], pos[1]), (self.GRID,self.GRID))
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, self.WHITE, rect, 1)


    def position_check(self,snake, food_group):
        for food in food_group:
            if snake.get_head_position() == food.position:
                snake.food_score += 1
                snake.length += 1
                food.randomize_food()


    def show_info(self,surface, snake):
        font = pygame.font.SysFont('malgungothic',30)
        image = font.render(f' food score : {snake.food_score} kill score: {snake.kill_score} ', True, self.WHITE)
        pos = image.get_rect()
        pos.move_ip(20,20)
        pygame.draw.rect(image, self.WHITE,(pos.x-20, pos.y-20, pos.width, pos.height), 2)
        surface.blit(image, pos)

        
    # ----- [Snake Class] -----

class Snake(Setting):

    def __init__(self):
        self.length = 1
        self.create_snake()
        self.color = self.BODY
        self.head_color = self.PLAYER
        self.life = True
        self.food_score = 0
        self.kill_score = 0
    def create_snake(self):
        self.length = 3
        self.positions = [(int(self.WINDOW_WIDTH/2), int(self.WINDOW_HEIGHT/2))]
        self.direction = random.choice([self.NORTH, self.SOUTH, self.WEST, self.EAST])
        self.food_score = 0
        self.kill_score = 0
    def move_snake(self,snake_list, surface):

        head = self.get_head_position()
        x, y = self.direction
        next = ((head[0] + (x*self.GRID)) % self.WINDOW_WIDTH, (head[1] + (y*self.GRID)) % self.WINDOW_HEIGHT)
        for sl in snake_list:
            if next in sl.positions[0:]:
                for sn in snake_list:
                    self.life = False
                return
        else:
            self.positions.insert(0, next)
            if len(self.positions) > self.length:
                del self.positions[-1]

    def draw_snake(self, surface):
        for index, pos in enumerate(self.positions):
            if index == 0:
                self.draw_object(surface, self.head_color, pos)
            else:
                self.draw_object(surface, self.color, pos)

    def respone(self,surface,mode):
        if self.life == False:
            self.life = True
            self.create_snake()
            self.gameover(surface,mode)               #endepisode

    def game_control(self, arrowkey):                           
        if (arrowkey[0]*-1, arrowkey[1]*-1) == self.direction:
            return
        else:
            self.direction = arrowkey

    def get_head_position(self):
        return self.positions[0]
    
    def gameover(self,surface,mode):
        print(mode)
        if mode == "play":
            font = pygame.font.SysFont('malgungothic',50)
            image = font.render('GAME OVER', True, self.WHITE)
            pos = image.get_rect()
            pos.move_ip(120,220)
            surface.blit(image, pos)
            pygame.display.update()
            time.sleep(2)
        else:
            #something about endepisode
            time.sleep(2)
    
    
    # ----- [Ai Snake Class] -----
class Ai_Snake(Setting):
    def __init__(self,snake_list):
        self.length = 1
        self.create_snake(snake_list)
        self.color = self.BODY
        self.head_color = self.AI
        self.life = True
        self.food_score = 0
        self.kill_score = 0
    def create_snake(self,snake_list):
        self.length = 3
        self.positions = [(-100,-100)]
        self.positions = [self.random_position(snake_list)]
        self.direction = random.choice([self.NORTH, self.SOUTH, self.WEST, self.EAST])
        self.food_score = 0
        self.kill_score = 0

    def random_position(self,snake_list):
        position = (random.randint(0,self.GRID_WIDTH-1)*self.GRID, random.randint(0,self.GRID_HEIGHT-1)*self.GRID)
        positionList = []
        for sl in snake_list:
            for ps in sl.positions:
                for i in range(4):
                    for j in range(4):
                        positionList.append((ps[0] + self.GRID*i, ps[1] + self.GRID*i))
                        positionList.append((ps[0] + self.GRID*i, ps[1] - self.GRID*i))
                        positionList.append((ps[0] - self.GRID*i, ps[1] + self.GRID*i))
                        positionList.append((ps[0] - self.GRID*i, ps[1] - self.GRID*i))
        positionList = list(set(positionList))
        if position in positionList:
            position = self.random_position(snake_list)
        
        return position
    
    def move_snake(self,snake_list, surface):

        head = self.get_head_position()
        x, y = self.direction
        next = ((head[0] + (x*self.GRID)) % self.WINDOW_WIDTH, (head[1] + (y*self.GRID)) % self.WINDOW_HEIGHT)
        for sl in snake_list:
            if next in sl.positions[0:]:
                self.life = False
                sl.kill_score += 1
                return
        self.positions.insert(0, next)
        if len(self.positions) > self.length:
            del self.positions[-1]

    def respone(self,snake_list):
        if self.life == False:
            self.life = True
            self.create_snake(snake_list)
            
    
    def draw_snake(self, surface):
        for index, pos in enumerate(self.positions):
            if index == 0:
                self.draw_object(surface, self.head_color, pos)
            else:
                self.draw_object(surface, self.color, pos)



    def game_control(self, arrowkey):                          
        if (arrowkey[0]*-1, arrowkey[1]*-1) == self.direction:
            return
        else:
            self.direction = arrowkey

    def get_head_position(self):
        return self.positions[0]    


    # ----- [ Food Class ] -----

class Food(Setting):
    def __init__(self):
        self.position =(0, 0)
        self.color = self.RED
        self.randomize_food()

    def randomize_food(self):
        self.position = (random.randint(0, self.GRID_WIDTH-1) * self.GRID,
                        random.randint(0, self.GRID_HEIGHT-1) * self.GRID)

    def draw_food(self, surface):
        self.draw_object(surface, self.color, self.position)



    # ----- [ Game Class ] -----
class SnakeGame(Snake, Ai_Snake):
    def __init__(self,set_game_mode = "play",set_ai_num = 10,set_food_num = 25, display: bool = True):
        self.game_mode = set_game_mode
        self.display = display
        self.run = True
        self.snake_group, self.ai_group, self.player = self.make_snakes(set_ai_num)
        self.food_group =  self.make_foods(set_food_num)
    
    def make_snakes(self,d_num):
        d_player = Snake()
        snake_list=[d_player]
        d_ai_list = []
        for i in range(d_num):                          #Control Ai Number
            d_ai = Ai_Snake(snake_list)
            snake_list.append(d_ai)
            d_ai_list.append(d_ai)
        return snake_list, d_ai_list, d_player
    

    def make_foods(self,d_num): # ----- [ Food Group ] -----
        d_food = Food()
        d_food_group = []
        for i in range(d_num):                          #Control Food Number
            d_food = Food()
            d_food_group.append(d_food)
        return d_food_group

    def draw_snake_group(self,snake_group,food_group, surface):
        for snake in snake_group:
            snake.move_snake(snake_group,surface)
            self.position_check(snake, food_group)
            snake.draw_snake(surface)
            if snake == snake_group[0]:
                snake.respone(surface,self.game_mode)
            else:
                snake.respone(snake_group)

    def draw_food_group(self,d_food_group, d_surface):
        for food in d_food_group:
            food.draw_food(d_surface)

    # ----- [ Game Loop ] -----
    def GameStart(self):


        if self.game_mode == "play":        #GamePlay
            pygame.init()
            pygame.display.set_caption('SNAKE GAME')
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            self.clock = pygame.time.Clock()
            while self.run:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if event.type == pygame.KEYDOWN:            #Get player input
                        if event.key == pygame.K_q:
                            self.run = False
                        if event.key == pygame.K_UP:
                            self.player.game_control(self.NORTH)
                        if event.key == pygame.K_DOWN:
                            self.player.game_control(self.SOUTH)
                        if event.key == pygame.K_RIGHT:
                            self.player.game_control(self.EAST)
                        if event.key == pygame.K_LEFT:
                            self.player.game_control(self.WEST)
                for ai in self.ai_group:
                    ai.game_control(random.choice([ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction, self.NORTH, self.SOUTH, self.WEST, self.EAST]))
                self.draw_background(self.screen)
                self.draw_snake_group(self.snake_group,self.food_group, self.screen)
                self.draw_food_group(self.food_group, self.screen)
                self.show_info(self.screen, self.player)                           
                # pygame.display.flip()
                pygame.display.update()
                #np_array = UpdateMap() 
                #print(np_array)
                self.clock.tick(20)

        else:               #training
            pygame.init()
            pygame.display.set_caption('SNAKE GAME')
            self.screen = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            self.clock = pygame.time.Clock()
            while self.run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if event.type == pygame.KEYDOWN:            
                        if event.key == pygame.K_q:
                            self.run = False
                
                discrete = 0   #Get discrete from agent dicrete = 0 ~ 3
                            
                self.player.game_control(self.get_direction(discrete))            
                for ai in self.ai_group:
                    ai.game_control(random.choice([ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction, self.NORTH, self.SOUTH, self.WEST, self.EAST]))
                self.draw_background(self.screen)
                self.draw_snake_group(self.snake_group,self.food_group, self.screen)
                self.draw_food_group(self.food_group, self.screen)                      
                np_array = self.UpdateMap(self.screen)     #3d image array 
                self.clock.tick(10)

        # ----- [ End Pygame ] -----

        print('pygame closed')
        pygame.quit()
        sys.exit()


    game_score = 0
    snake_list = []
    
    def start(self):
        pygame.init()
        pygame.display.set_caption('SNAKE GAME')
        if self.display:
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        else:
            self.screen = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
    
    def set_move(self, move_action: str):
        if move_action == "up":
            self._direction = self.NORTH
        elif move_action == "down":
            self._direction = self.SOUTH
        elif move_action == "left":
            self._direction = self.WEST
        elif move_action == "right":
            self._direction = self.EAST
        else:
            raise ValueError(f"Invalid move action: {move_action}")
        
    def update(self):
        self.player.game_control(self._direction)            
        for ai in self.ai_group:
            ai.game_control(random.choice([ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction,ai.direction, self.NORTH, self.SOUTH, self.WEST, self.EAST]))
        self.draw_background(self.screen)
        self.draw_snake_group(self.snake_group,self.food_group, self.screen)
        self.draw_food_group(self.food_group, self.screen)       
        if self.display:
            self.show_info(self.screen, self.player)                           
            # pygame.display.flip()
            pygame.display.update()               
        self._screen_image = self.UpdateMap(self.screen)     #3d image array 
        self.clock.tick(60)
        
    def close(self):
        pygame.quit()
        
    @property
    def screen_image(self) -> np.ndarray:
        return self._screen_image
    
    @property
    def game_over(self) -> bool:
        return not self.player.life
    
# sg = SnakeGame("play")

# sg.GameStart()