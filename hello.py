import pygame

pygame.init()

window = pygame.display.set_mode((800, 480))

pygame.display.set_caption("Who Killed M?")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
backGround = pygame.image.load('backGround.png')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, window):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                window.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            else:
                window.blit(walkLeft[0], (self.x, self.y))
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(window, (255,0,0), self.hitBox,2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 415
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 200)
        text = font1.render('-2', 1, (255, 0, 0))
        window.blit(text, (400 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, colour, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 2
        self.hitBox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, window):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(window, (255, 0, 0), (self.hitBox[0], self.hitBox[1] - 20, 50, 10))
            pygame.draw.rect(window, (0, 128, 0),
                             (self.hitBox[0], self.hitBox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitBox = (self.x + 17, self.y + 2, 31, 57)
            pygame.draw.rect(window, (255, 0, 0), self.hitBox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        # print('hit')


def redrawGamewindowdow():
    window.blit(backGround, (0, 0))
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    window.blit(text, (350, 10))
    mc.draw(window)
    goblin.draw(window)
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()


# mainloop
font = pygame.font.SysFont('comicsans', 30, True)
mc = player(100, 415, 64, 64)
goblin = enemy(400, 415, 64, 64, 700)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if goblin.visible:
        if mc.hitBox[1] < goblin.hitBox[1] + goblin.hitBox[3] and mc.hitBox[1] + mc.hitBox[3] > goblin.hitBox[1]:
            if mc.hitBox[0] + mc.hitBox[2] > goblin.hitBox[0] and mc.hitBox[0] < goblin.hitBox[0] + goblin.hitBox[2]:
                mc.hit()
                score -= 2

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitBox[1] + goblin.hitBox[3] and bullet.y + bullet.radius > goblin.hitBox[
            1]:
            if bullet.x + bullet.radius > goblin.hitBox[0] and bullet.x - bullet.radius < goblin.hitBox[0] + \
                    goblin.hitBox[2]:
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if 800 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if mc.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 3:
            bullets.append(
                projectile(round(mc.x + mc.width // 2), round(mc.y + mc.height // 2), 6, (0, 0, 0), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and mc.x > mc.vel:
        mc.x -= mc.vel
        mc.left = True
        mc.right = False
        mc.standing = False
    elif keys[pygame.K_RIGHT] and mc.x < 800 - mc.width - mc.vel:
        mc.x += mc.vel
        mc.right = True
        mc.left = False
        mc.standing = False
    else:
        mc.standing = True
        mc.walkCount = 0

    if not mc.isJump:
        if keys[pygame.K_UP]:
            mc.isJump = True
            mc.right = False
            mc.left = False
            mc.walkCount = 0
    else:
        if mc.jumpCount >= -10:
            neg = 1
            if mc.jumpCount < 0:
                neg = -1
            mc.y -= (mc.jumpCount ** 2) * 0.5 * neg
            mc.jumpCount -= 1
        else:
            mc.isJump = False
            mc.jumpCount = 10

    redrawGamewindowdow()

pygame.quit()
