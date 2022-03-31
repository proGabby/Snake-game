import pygame
from pygame.locals import *
from pygame import font, time, mixer
import random

SIZE = 40
class Apple:
    def __init__(self,parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120
    
    def apple_draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x= random.randint(0,10)*SIZE
        self.y=random.randint(0,9)*SIZE


    
class Snake:
    def __init__(self, parent_screen, length:int):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = "right"

        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    
    def move_up(self):
        if not self.direction == "down":
            self.direction = "up"
    def move_down(self):
        if not self.direction == "up":
            self.direction = "down"
    
    def move_right(self):
        if not self.direction == "left":
            self.direction = "right"
    
    def move_left(self):
        if not self.direction == "right":
            self.direction = "left"

    def walk(self):
        for j in range(self.length-1,0,-1):
            self.x[j] = self.x[j-1]
            self.y[j] = self.y[j-1]

        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw_snake()
    
    def background_img(self):
        bck_img = pygame.image.load("resources/green-grass.jpg").convert()
        self.parent_screen.blit(bck_img,(0,0))
    
    def draw_snake(self):
        self.background_img()
        for i in range(self.length):
            self.parent_screen.blit(self.image,(self.x[i],self.y[i]))
        pygame.display.flip()

    
    def increase_snake_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    
    def out_of_screen(self):
        if self.x[0] > 1000:
            self.x[0]=5
            for i in range(1,self.length):
                self.x[i]= self.x[i-1]

        if self.x[0] < 0:
            self.x[0]=1000
            for i in range(1,self.length):
                self.x[i]= self.x[i-1]

        if self.y[0] < 0:
            self.y[0]=500
            for i in range(1,self.length):
                self.y[i]= self.y[i-1]

        if self.y[0] > 500:
            self.y[0]= 0
            for i in range(1,self.length):
                self.y[i]= self.y[i-1]
    

class Game:

    def __init__(self):
        pygame.init()
        self.parent_screen = pygame.display.set_mode((1000,500))
        pygame.mixer.init()
        self.bg_music()
        self.parent_screen.fill("green")
        pygame.display.set_caption("Anaconda's World by WILLIE")
        self.snake = Snake(self.parent_screen,1)
        self.snake.draw_snake()
        self.apple = Apple(self.parent_screen)
        self.apple.apple_draw()
        self.game_score = 1
        self.pause = False

    def collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False    


    def display_score(self):

        font_ = font.SysFont("Arial", 30)
        if self.snake.length == 1:
            score_=font_.render(f"Game Score: {1}",True,(200,200,200))
        if self.snake.length >1:
            self.game_score = (self.snake.length-1)*15
            score_=font_.render(f"Game Score: {self.game_score}",True,(200,200,200))
        self.parent_screen.blit(score_,(700,10))
        

    def play(self):
        
        if self.pause == False:
            self.snake.walk()
        
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y)== True:
            eating_sound = pygame.mixer.Sound("resources/Bite-sound-effect.mp3")
            mixer.Sound.play(eating_sound)
            self.snake.increase_snake_length()
            self.apple.move()  
        
        self.apple.apple_draw()

        self.display_score()
        self.pause_button()

        
        for i in range(3,self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                biting_self = mixer.Sound("resources/Scream-Sound.mp3")
                mixer.Sound.play(biting_self)
                raise "Game Over"

        
        self.snake.out_of_screen()
        pygame.display.flip()
    
    
    # def out_sight(self):
    #     result = True
    #     if self.snake.length>1:
    #         if self.snake.x[0]>1000 or self.snake.x[0]<0 or self.snake.x[(self.snake.length-1)]>1000 or self.snake.x[(self.snake.length-1)]<0:
    #             result = False
    #     return result
            
                

    def game_failed(self):
        font_ = font.SysFont("Arial", 25)
        display1 = font_.render(f"YOU HAVE FAILED. YOUR SCORE IS {self.game_score}", True, (200,200,200))
        display2 = font_.render(f"PRESS ENTER TO RETRY AND ESCAPE TO QUIT", True, (200,200,200))
        self.parent_screen.blit(display1, (200,200))
        self.parent_screen.blit(display2, (200,250))
        mixer.music.stop()
    
    def pause_button(self):
        font_ = font.SysFont("Arial", 30)
        pause_ = font_.render(f"PAUSE",True,(200,200,200))
        self.parent_screen.blit(pause_,(0,0))
    
    def play_notice(self):
        font_=font.SysFont("Arial", 20)
        play_notice_display = font_.render(f"CLICK OUTSIDE 'PAUSE' TO RESUME",True,(200,200,200))
        self.parent_screen.blit(play_notice_display,(300,250))
        pygame.display.flip()
    
    def restart_game(self):
        self.snake = Snake(self.parent_screen,1)
        self.apple = Apple(self.parent_screen)
        mixer.music.play()

    def game_speed(self):
        if self.game_score<200:
            speed = 2
        elif self.game_score<500:
            speed = 5
        elif self.game_score>500:
            speed = 7
        time.wait((500//speed))

    def bg_music(self):
        bg_sound = mixer.music.load("resources/kiki.mp3")
        mixer.music.play(-1)
        


    def run(self):
        running = True
        failed = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running=False

                (t, s)= pygame.mouse.get_pos()
                if event.type== MOUSEBUTTONDOWN:
                    if t<100and s<40:
                        self.pause = True
                        mixer.music.pause()
                        self.play_notice()
                    else:
                        self.pause = False
                        mixer.music.unpause()
    
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        failed = False
                        self.restart_game()
                        
                    if event.key == K_ESCAPE:
                        running = False
                    if not failed:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_LEFT:
                            self.snake.move_left()
            

            try:
        
                if not failed:
                    self.play()
            except Exception:
                self.game_failed()
                pygame.display.flip()
                failed= True
            
            self.game_speed()

game = Game()
game.run()