import pygame as py 
import random


class Player:
    def __init__(self, pos:list, player1=True):
        self.pos = pos
        self.rect = py.FRect(self.pos, (10, 100)) # Bar Rect

        self.player1 = player1

    def move(self) :
        # get pressed keys
        keys = py.key.get_pressed()
        
        if self.player1:
            if keys[py.K_s]: # move down
                self.pos[1] += 3
            elif keys[py.K_w]: # move up
                self.pos[1] -= 3
        else:
            if keys[py.K_DOWN]: # move down
                self.pos[1] += 3
            elif keys[py.K_UP]: # move up
                self.pos[1] -= 3
        
        # limit vertical space
        if self.pos[1] < 0:
            self.pos[1] = 0
        elif self.pos[1] + self.rect.h > window.get_height():
            self.pos[1] = window.get_height() - self.rect.h

        self.rect.topleft = self.pos
        
    def draw(self):
        py.draw.rect(window, (100, 100, 100), self.rect, border_radius=5)

    def update(self):
        self.move()

class Ball:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 10 # ball radius

        self.movement = [random.randint(0, 1), random.randint(0, 1)]
        self.vel = [0, 0]
    
    def move(self):
        # horizotal movement
        if self.movement[0]:
            self.vel[0] = 5 # move right
        elif not self.movement[0]:
            self.vel[0] = -5 # move left
        
        # vertical movement
        if self.movement[1]:
            self.vel[1] = 5 # move down
        elif not self.movement[1]:
            self.vel[1] = -5 # move up

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    
    def collision(self, players:list):
        for player in players:

            if player.rect.collidepoint(self.pos):
                # horizontal collision
                if self.movement[0]:
                    self.movement[0] = 0
                elif not self.movement[0]:
                    self.movement[0] = 1
        
        if self.pos[1] - self.radius < 0:
            self.movement[1] = 1
        elif self.pos[1] > window.get_height() - self.radius:
            self.movement[1] = 0

    def game_state(self):
        if self.pos[0] == 0 or self.pos[0] == window.get_width():
            return True
        return False

    def draw(self):
        py.draw.circle(window, (100, 100, 100), self.pos, self.radius)

    def update(self):
        self.move()
        self.collision

py.init()
py.display.set_caption('Ping Pong')

# window
window = py.display.set_mode((800, 600))
clock = py.time.Clock()
font = py.font.Font(None, 32)

# players and obj
player1 = Player([0, window.get_height()/2])
player2 =  Player([window.get_width() - 10, window.get_height()/2], False)
ball = Ball([window.get_width()/2, window.get_height()/2])

# program state
running = True
lost = False # game state
ready = False # start up 

# lost msg
lost_msg = font.render('Lost!', True, (150, 150, 150))
lost_msg_rect = lost_msg.get_rect(center=[window.get_width()/2, window.get_height()/2 - 32])

# ready msg
ready_msg = font.render('Click to play', True, (150, 150, 150))
ready_msg_rect = ready_msg.get_rect(center=[window.get_width()/2, window.get_height()/2 - 32])

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    
    window.fill((30, 30, 30))

    # check game state
    if not lost:

        # check start up
        if ready:
            player1.update()
            player2.update()
            ball.update()
            ball.collision([player1, player2])
            lost = ball.game_state()
        else:
            window.blit(ready_msg, ready_msg_rect)
            if py.mouse.get_pressed()[0]:
                ready = True
    else:   
        window.blit(lost_msg, lost_msg_rect)
        if py.mouse.get_pressed()[0]:
            lost = False

            # restart
            player1 = Player([0, window.get_height()/2])
            player2 =  Player([window.get_width() - 10, window.get_height()/2], False)
            ball = Ball([window.get_width()/2, window.get_height()/2])
    
    player1.draw()
    player2.draw()
    ball.draw()
    
    py.display.update()
    clock.tick(60)

py.quit()