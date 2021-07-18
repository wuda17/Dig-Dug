import pygame,time,sys
pygame.init()
pygame.key.set_repeat(1, 10)


size = screen_width, screen_height = 700, 900
screen = pygame.display.set_mode(size)


pygame.display.set_caption('DIG DUG')

walkRight = [pygame.image.load('R1.png'),pygame.image.load('R2.png')]
walkLeft = [pygame.image.load('L1.png'),pygame.image.load('L2.png')]
walkUp = [pygame.image.load('U1.png'),pygame.image.load('U2.png')]
walkDown = [pygame.image.load('D1.png'),pygame.image.load('D2.png')]

#Colours
black = [0, 0, 0]
white = [255, 255, 255]
green = [0, 255, 0]
orange = [240,128,128]
dirt = [220,20,60]
blue = [0,0,128]


grid=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,1,0,0,0,0,0,0,0,1,1,1,1,0],
      [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
      [0,0,1,1,1,1,0,0,0,1,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,1,0,0,0,0],
      [0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

colour=[orange,black,blue]

#Live Graphic

lives1 = pygame.image.load('R1.png')
lives1rect = lives1.get_rect()
lives1rect.left = (10)
lives1rect.top = (850)

lives2 = pygame.image.load('R1.png')
lives2rect = lives2.get_rect()
lives2rect.left = (60)
lives2rect.top = (850)

lives3 = pygame.image.load('R1.png')
lives3rect = lives3.get_rect()
lives3rect.left = (110)
lives3rect.top = (850)

lives4 = pygame.image.load('R1.png')
lives4rect = lives4.get_rect()
lives4rect.left = (160)
lives4rect.top = (850)

lives = [lives1rect, lives2rect, lives3rect, lives4rect]

#TEXTS / FONT 
font = pygame.font.SysFont('Terminal', 28)
renderedtext1 = font.render("GAME OVER. PRESS Q TO QUIT OR R TO RETRY...", 1, white)
renderedtext3 = font.render("WELCOME TO DIG DUG BETA", 1, white)
renderedtext4 = font.render("A MODERN REMAKE OF THE ARCADE CLASSIC. WITH A TWIST.", 1, white)
renderedtext5 = font.render("Press s to Start, or q to Quit.", 1, white)
renderedtext6 = font.render("THE TWIST: You have no weapon. The Pookas cannot be killed...", 1, white)

clock = pygame.time.Clock()

score = 0

#Player
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.run = 4
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True
        self.walkCount = 0 
        self.dx = 0
        self.dy = 0
        self.hitbox = (self.x, self.y, 48, 52)

    def draw(self,screen):
        if self.walkCount >= 6:
            self.walkCount = 0 

        if not (self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
                
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

                
            elif self.down:
                screen.blit(walkDown[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

                
            elif self.up:
                screen.blit(walkUp[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1

        else:
            if self.right:
                screen.blit(walkRight[0], (self.x,self.y))
            elif self.left:
                screen.blit(walkLeft[0], (self.x,self.y))
            elif self.down:
                screen.blit(walkDown[0], (self.x,self.y))
            elif self.up:
                screen.blit(walkUp[0], (self.x,self.y))
            else:
                screen.blit(walkRight[0], (self.x,self.y))
        self.hitbox = (self.x, self.y-2, 48, 48) 
#Show Hitbox
        pygame.draw.rect(screen, white, self.hitbox,2)

    def hit(self):
        self.x = 350
        self.y = 54
        self.walkCount = 0
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()


        
#Enemy : POOKA
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png')]

    def __init__(self, x, y, width, height, end, dirxy):
        self.x = x
        self.y = y
        self. width = width
        self.height = height
        self.end = end
        
        self.walkCount = 0
        self.run = 3
        self.hitbox = (self.x, self.y - 5, 48, 48)
        self.dirxy=dirxy

        if self.dirxy=="x":
            self.path = [self.x, self.end]
        else:
            self.path = [self.y, self.end]
            
    def draw(self,screen):
        self.move()
        if self.walkCount + 1 >= 18:
            self.walkCount = 0 

        if self.run > 0:
            screen.blit(self.walkRight[self.walkCount//9], (self.x, self.y))
            self.walkCount += 1
        else:
            screen.blit(self.walkLeft[self.walkCount//9], (self.x, self.y))
            self.walkCount += 1


    def move(self):
        if self.dirxy=="x":
            if self.run > 0:
                if self.x + self.run < self.path[1]:
                    self.x += self.run
                else:
                    self.run = self.run * -1
                    self.walkCount = 0
            else:
                if self.x - self.run > self.path[0]:
                    self.x += self.run
                else:
                    self.run = self.run * -1
                    self.walkCount = 0
        else:
            if self.run > 0:
                if self.y + self.run < self.path[1]:
                    self.y += self.run
                else:
                    self.run = self.run * -1
                    self.walkCount = 0
            else:
                if self.y - self.run > self.path[0]:
                    self.y += self.run
                else:
                    self.run = self.run * -1
                    self.walkCount = 0
            
        self.hitbox = (self.x, self.y + 2, 48, 40)
#Showing Hitboxes
        #pygame.draw.rect(screen, white, self.hitbox,2)
        
    

def redrawgamewindow():
#Creating the Ground as a Grid
    r=100
    c=0
    for row in grid: 
        for cell in row:
            pygame.draw.rect(screen,colour[cell],pygame.Rect(c,r,50,50),0)
            c+=50
        r+=50
        c=0

    for i in range (0,900,50):
        pygame.draw.line(screen,black,[i,900],[i,0])
        pygame.draw.line(screen,black,[0,i],[900,i])


    pygame.draw.rect(screen,blue,(0, 0, 700, 100))
    pygame.draw.rect(screen,black,(0, 850, 700, 50))

    renderedtext2 = font.render('Score: ' + str(score), 1, white)
    screen.blit(renderedtext2, (150, 30))
    
    for l in lives:
        screen.blit(lives1,l)
        

    dig.draw(screen)
    for pooka in pookas:
        pooka.draw(screen)
    

    if gameOver:
        screen.fill(black)
        screen.blit(renderedtext1, (50,screen_height/2-20))
    
    pygame.display.update()


    

    
dig = player(350, 54, 50, 50)
pookas  = [enemy(450, 205, 50, 50, 600, "x"), 
    enemy(100, 605, 50, 50, 250, "x"), 
    enemy(50, 200, 50, 50, 400, "y"), 
    enemy(450, 550, 50, 50, 750, "y")]


bullets = []

gamerun = False
gameOver = False

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys=pygame.key.get_pressed()

        if keys[pygame.K_s]:
            intro = False
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
            
        screen.fill(dirt)
        pygame.draw.rect(screen,blue,(0, 0, 700, 100))
        pygame.draw.rect(screen,black,(0, 850, 700, 50))


        screen.blit(renderedtext3, (220, 200))
        screen.blit(renderedtext4, (70, 230))
        screen.blit(renderedtext5, (220, 600))
        screen.blit(renderedtext6, (60, 700))
        pygame.display.update()
        clock.tick(24)

game_intro()
gamerun = True
while gamerun:
    clock.tick(24)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False

            
    keys=pygame.key.get_pressed()


    for pooka in pookas:
        if dig.hitbox[1] < pooka.hitbox[1] + pooka.hitbox[3] and dig.hitbox[1] + dig.hitbox[3] > pooka.hitbox[1]:
            if dig.hitbox[0] + dig.hitbox[2] > pooka.hitbox[0] and dig.hitbox[0] < pooka.hitbox[0] + pooka.hitbox[2]:
                dig.hit()
                score -= 100
                lives.pop()
    if gameOver:
        if keys[pygame.K_r]:
            gameOver = False
            lives = [lives1rect, lives2rect, lives3rect, lives4rect]
            score = 0
            screen.fill(black)
            screen.blit(renderedtext1, (50,screen_height/2-20))
            pygame.display.update()
            
            
        elif keys[pygame.K_q]:
            gamerun = False


    if keys[pygame.K_LEFT] and dig.x > 55 - dig.width :
        dig.x -= dig.run
        dig.dx= 0
        dig.dy= dig.height//2
        dig.left = True
        dig.up = False
        dig.down = False
        dig.right = False
        dig.standing = False

    elif  keys[pygame.K_RIGHT] and dig.x < 700 - dig.width:
        dig.x += dig.run
        dig.dx = dig.width
        dig.dy = dig.height//2
        dig.left = False
        dig.down = False
        dig.right = True
        dig.standing = False

    elif keys[pygame.K_UP] and dig.y > 104 - dig.height:
        dig.y -= dig.run
        dig.dy= 0
        dig.dx= dig.width//2
        dig.left = False
        dig.right = False
        dig.up = True
        dig.down = False
        dig.standing = False 

    elif keys[pygame.K_DOWN] and dig.y < 850 - dig.height:
        dig.y += dig.run
        dig.dy = dig.height-5
        dig.dx = dig.width//2
        dig.left = False
        dig.right = False
        dig.up = False
        dig.down = True
        dig.standing = False

    else:
        dig.standing = True
        dig.walkCount = 0 

#Creating the Tunnels                        
    c=(dig.x + dig.dx - 1)//50
    r=(dig.y + dig.dy-100)//50
    if r >= 0:
        if grid[r][c]!=1:
            score += 10
        grid[r][c]=1


    if len(lives) == 0:
        gameOver = True

    redrawgamewindow()

pygame.quit()
sys.exit()
