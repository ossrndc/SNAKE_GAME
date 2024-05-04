import pygame as oss
from pygame.locals import *
import time 
import random


SIZE = 60
BACKGROUND_COLOR = (52, 235, 82)

class WelcomeScreen:
    def __init__(self, surface):
        self.surface = surface

    def show_welcome(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = oss.font.SysFont('arial', 60)
        welcome_message = font.render("Welcome to world of snake!", True, (255, 0, 0))
        instructions1 = font.render("Press Q to start the game.", True, (255, 0, 0))
        
        self.surface.blit(welcome_message, (200, 300))
        self.surface.blit(instructions1, (200, 400))
       
        oss.display.flip()

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in oss.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        waiting = False
                    elif event.key == K_w:
                        oss.quit()
                        self.exit()
class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = oss.image.load("./apple.jpg.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        oss.display.flip()

    def move(self):
        self.x = random.randint(1,16)*SIZE
        self.y = random.randint(1,11)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = oss.image.load("./block.jpg.png").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [60]
        self.y = [60]

    def move_left(self):
        if self.direction!='right' or self.length==1:
            self.direction = 'left'

    def move_right(self):
        if self.direction!='left' or self.length==1:
            self.direction = 'right'

    def move_up(self):
        if self.direction!='down' or self.length==1:
            self.direction = 'up'

    def move_down(self):
        if self.direction!='up' or self.length==1:
            self.direction = 'down'

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        oss.display.flip()

    def increase_length(self):
        #increase length of the snake

class PLAY:
    def __init__(self):
        oss.init()

        oss.mixer.init()
        self.play_background_music()

        self.surface = oss.display.set_mode((1000, 690))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.speed=0.25

    def play_background_music(self):
        oss.mixer.music.load("./enigma-dream-170618.mp3")
        oss.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == 'beep':
            sound = oss.mixer.Sound("./beep.mp3.mp3")
        elif sound_name == 'beep':
            sound = oss.mixer.Sound("./beep.mp3.mp3")

        oss.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        #add collision of snake on  boundary
        if (x1==x2 and y1==y2):
            return True
        return False

    def is_out_of_bounds(self):
        if (self.snake.x[0]<0
            or self.snake.x[0]>=1000
            or self.snake.y[0]<0
            or self.snake.y[0]>=690):
            return True
        return False
    def render_background(self):
        bg = oss.image.load("./background.jpg.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        oss.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("beep")
            self.snake.increase_length()
            self.apple.move()
            i=1
            while i<self.snake.length:
                if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                    self.apple.move()
                    i=1
                else:
                    i+=1

        if self.is_out_of_bounds():
            self.play_sound('beep')
            raise "out of bounds"
        
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('beep')
                raise "Collision Occurred"

    def display_score(self):
        font = oss.font.SysFont('arial',60)
        score = font.render(f"Score: {self.snake.length}",True,(255,0,0))
        self.surface.blit(score,(650,10))

    
        
    def show_game_over(self):
        self.render_background()
        font = oss.font.SysFont('arial', 60)
        line1 = font.render(f" Your score is {self.snake.length}", True, (255, 0, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter.", True, (255, 0, 0))
        self.surface.blit(line2, (200, 350))
        line3 = font.render("TO exit press Escape!", True ,(255,0,0))
        self.surface.blit(line3, (200,400))
        oss.mixer.music.pause()
        oss.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in oss.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        oss.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()
                    

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time .sleep(self.speed)

if __name__ == '__main__':
    oss.init()
    surface = oss.display.set_mode((1000, 690))
    oss.display.set_caption('Snake Game')
    oss.display.set_icon(oss.image.load(r"./game_icon.png"))
    welcome = WelcomeScreen(surface)
    welcome.show_welcome()
    welcome.wait_for_key()
    game = PLAY()
    game.run()
   