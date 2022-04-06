import pygame
from random import random

class Game:
	def __init__(self):
		self.model = Model()
		self.view = View(self.model)
		self.controller = Controller(self.model)

		pygame.init()

		self.running = True
		self.clock = pygame.time.Clock()

	def run(self):
		while self.running:
			self.update()

	def update(self):
		#print("Works")
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

		self.controller.update()
		self.model.update()
		self.view.update()

		self.clock.tick(40)

class Model:
	def __init__(self):
		
		self.mario = Mario(550, 300)
		
		self.brick = Brick(-50, 30, "reg")
		self.brick1 = Brick(-50, 350, "reg")
		self.brick2 = Brick(500, 30, "coinb")
		self.brick3 = Brick(250, 30, "reg")
		self.brick4 = Brick(800, 30, "coinb")
		self.brick5 = Brick(800, 350, "reg")

		self.cameraPos = self.mario.x

		self.sprites = []
		self.sprites.append(self.mario)

		self.sprites.append(self.brick)
		self.sprites.append(self.brick1)
		self.sprites.append(self.brick2)
		self.sprites.append(self.brick3)
		self.sprites.append(self.brick4)
		self.sprites.append(self.brick5)

	def coinDeleter(self):
		for sprite in self.sprites:
			if sprite.y > 600:
				self.sprites.remove(sprite)
				#print(self.sprites)

	def update(self):
		self.cameraPos = self.mario.x
		self.coinDeleter()

		for  sprite in self.sprites:
			sprite.update()
			sprite.updateSides()
			if sprite.stype == "brick" and self.checkCollisions(self.mario, sprite):
				self.collisionGetOut(self.mario, sprite)

	def checkCollisions(self, collider1, collider2):
		if(collider1.right < collider2.left or
	       collider1.bot < collider2.top or
		   collider1.top > collider2.bot or 
		   collider1.left > collider2.right):
			return False
		else:
			return True
	
	def collisionGetOut(self, collider1, collider2):
		leftCollision = abs(collider1.left - collider2.right)
		botCollision = abs(collider1.top - collider2.bot)
		topCollision = abs(collider2.top - collider1.bot)
		rightCollision = abs(collider2.left - collider1.right)
		maxCollision = max(leftCollision, botCollision, topCollision, rightCollision)

		if leftCollision == maxCollision:
			collider1.x = collider2.left - collider1.w 

		if rightCollision == maxCollision:
			collider1.x = collider2.right

		if botCollision == maxCollision:
			collider1.y = collider2.top - collider1.h		
			self.mario.vertVel = 0
			self.mario.CounterJ = 0

		if topCollision == maxCollision:
			collider1.y = collider2.bot 
			self.mario.vertVel = 0
			if collider2.btype == "coinb":
				self.sprites.append(Coin(collider2.x, collider2.y))
				collider2.totalCoins -= 1
				#print(self.sprites)

class Controller:
	def __init__(self, model):
		self.model = model

		self.keyRight = False
		self.keyUp = False
		self.keyLeft = False

	def update(self):
		self.keyRight = pygame.key.get_pressed().__getitem__(pygame.K_RIGHT)
		self.keyUp = pygame.key.get_pressed().__getitem__(pygame.K_SPACE) or pygame.key.get_pressed().__getitem__(pygame.K_UP)
		self.keyLeft = pygame.key.get_pressed().__getitem__(pygame.K_LEFT)

		mario = self.model.mario 

		if self.keyUp and mario.CounterJ == 0:
			mario.vertVel -= 35

		if self.keyRight:
			mario.x += 10
			#self.model.cameraPos += 10
			mario.currentAnimation += 1
			if mario.currentAnimation > 4:
				mario.currentAnimation = 0

		if self.keyLeft:
			mario.x -= 10
			#self.model.cameraPos -= 10

			mario.currentAnimation += 1
			if mario.currentAnimation > 4:
				mario.currentAnimation = 0

class View:
	size = width, height = 1200, 600
	
	def __init__(self,model):
		self.model = model
		self.screen = pygame.display.set_mode(self.size)
		self.screen.fill((0,0,0))

		self.backgroundImage = pygame.image.load("background.png")
		self.backgroundImage = pygame.transform.smoothscale(self.backgroundImage, (12800, 720))

		self.groundImage = pygame.image.load("ground.png")
		self.groundImage = pygame.transform.smoothscale(self.groundImage, (3000, 100))

	def update(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.backgroundImage, (-self.model.cameraPos/2 - Mario.MarioPosition, 0))
		self.screen.blit(self.groundImage, (-self.model.cameraPos - Mario.MarioPosition, 500))
        
		for sprite in self.model.sprites:
			sprite.drawImages(self.screen, self.model.cameraPos)
		
		pygame.display.update()

class Sprite:
	def __init__(self, x, y, w, h, stype):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.stype = stype

	def update(self):
		pass
	
	def loadImages(self, file_name):
		temp = pygame.image.load(file_name)
		temp = pygame.transform.smoothscale(temp, (self.w, self.h))
		self.images.append(temp)


	def drawImages(self, screen, cameraPos):
		pass

	def updateSides(self):
		self.top = self.y
		self.bot = self.y + self.h
		self.left = self.x
		self.right = self.x + self.w		
		
class Mario(Sprite):
	MarioPosition = 0
	def __init__(self, x, y):
		super().__init__(x, y, 60, 95, "mario")

		self.images = []
		self.loadImages("mario1.png")
		self.loadImages("mario2.png")
		self.loadImages("mario3.png")
		self.loadImages("mario4.png")
		self.loadImages("mario5.png")

		Mario.MarioPosition = self.x

		self.vertVel = 0
		self.CounterJ = 0
		self.currentAnimation = 0

	def drawImages(self, screen, cameraPos):
		screen.blit(self.images[self.currentAnimation], (Mario.MarioPosition, self.y))

	def update(self):
		self.vertVel += 2.1
		self.y += self.vertVel
		if self.y > 400:
			self.vertVel = 0
			self.y = 400
			self.CounterJ = 0
		else:
			self.CounterJ = self.CounterJ + 1

class Brick(Sprite):
	def __init__(self, x, y, btype):
		super().__init__(x, y, 200, 200, "brick")

		self.currentImage = 0
		self.images = []
		self.loadImages("brick.png")
		self.loadImages("block1.png")
		self.loadImages("block2.png")

		self.totalCoins = 5

		self.btype = btype
		if self.btype == ("coinb"):
			self.currentImage = 1	

	def drawImages(self, screen, cameraPos):
		screen.blit(self.images[self.currentImage], (self.x - cameraPos + Mario.MarioPosition, self.y))

	def update(self):
		if self.btype == "coinb" and self.totalCoins == 0:
			self.btype = "emptyb"
			self.currentImage = 2

class Coin(Sprite):
	def __init__(self, x, y):
		super().__init__(x, y, 200, 200, "coin")

		self.currentImage = 0
		self.images = []
		self.loadImages("coin.png")
		
		self.max = 25
		self.min = -25
		self.range = self.max - self.min
		self.horVel = ((random() * self.range) - self.range/2)
		self.vertVel = -20

	def drawImages(self, screen, cameraPos):
		screen.blit(self.images[self.currentImage], (self.x - cameraPos + Mario.MarioPosition, self.y))

	def update(self):
		self.x += self.horVel
		self.vertVel += 2.1
		self.y += self.vertVel

game = Game()
game.run()
