import pygame
import os
import time
import random
pygame.init()

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
WIDTH = 1200
HEIGHT = 700
clock = pygame.time.Clock()

#displaying screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()

#initializing font for writing level and health
FONT = pygame.font.SysFont('Verdana', 20)
END_FONT = pygame.font.SysFont('Comic Sans MS', 70)

#loading in images/sound for player
player_image = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'tank.png')),(80, 30)).convert_alpha()
player_height = player_image.get_height()
player_width = player_image.get_width()
player_blaster_sound = pygame.mixer.Sound(os.path.join('sounds', 'player_blaster.wav'))
death_sound = pygame.mixer.Sound(os.path.join('sounds', 'death_sound.wav'))

#loading images/sound for enemy
enemy_image = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'enemy.png')),(40, 30)).convert_alpha()
enemy_width = enemy_image.get_width()
enemy_height = enemy_image.get_height()
enemy_blaster_sound = pygame.mixer.Sound(os.path.join('sounds', 'enemy_blaster.wav'))

#loading in background
bg = pygame.transform.scale(pygame.image.load(os.path.join('pictures', 'Background.png')), (WIDTH, HEIGHT))

#transition sounds
win_sound = pygame.mixer.Sound(os.path.join('sounds', 'win_sound.wav'))
lose_sound = pygame.mixer.Sound(os.path.join('sounds', 'lose_sound.wav'))
level_sound = pygame.mixer.Sound(os.path.join('sounds', 'next_level_sound.wav'))
welcome_sound = pygame.mixer.Sound(os.path.join('sounds', 'welcome_sound.wav'))

#setting title
pygame.display.set_caption('Space Invaders UWU')

class Ship:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.speed = 5

class Laser:
	#for speed of enemy laser, will be modified as level increases
	enemy_fire_speed = 2
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.speed = 15


class Alien:
	def __init__(self, x, y):
		self.x = x
		self.y = y

#check if alien touch edge
def edge_check(WIDTH, enemy_list):
	global delta
	global Alien_speed
	count =[]
	for enemies in enemy_list:
		if (enemies.x + enemy_width + Alien_speed >= WIDTH) or (enemies.x + Alien_speed <= 0):
			count.append(True)
	if True in count:
		delta += 20
		Alien_speed *= -1


#sound might be loud be careful
def warning_sign(FONT, SCREEN):
	warning = FONT.render(('SOUND WARNING \n WIN AFTER 6 ROUNDS'), 1, WHITE)
	warning_length = warning.get_width()
	SCREEN.blit(warning,(WIDTH//2 - warning_length/2, HEIGHT//2))
	pygame.display.update()
	time.sleep(3)

def display_lives_level(FONT, SCREEN):
	global LIVES
	global LEVEL
	Lives_text = FONT.render(f'LIVES: {LIVES}', 1, WHITE) 
	Level_text = FONT.render(f'LEVEL: {LEVEL}', 1 , WHITE)
	Level_width = Level_text.get_width()
	SCREEN.blit(Lives_text, (10,0))
	SCREEN.blit(Level_text, ((WIDTH - Level_width - 10), 0))

#display for when game is lost
def display_loser(END_FONT, SCREEN, FPS):
	global RUN
	global end_timer
	lose_sign = END_FONT.render('LOSER',1, WHITE)
	lose_width = lose_sign.get_width()
	SCREEN.blit(lose_sign, (WIDTH/2 - lose_width/2, HEIGHT/2))
	if end_timer == 0:
		lose_sound.play()
	end_timer += 1
	if end_timer >= (FPS * 4):
		RUN = False

#display for when game is won
def display_winner(END_FONT, SCREEN, FPS):
	global RUN
	global end_timer
	win_sign = END_FONT.render('WINNER',1, GREEN)
	win_width = win_sign.get_width()
	SCREEN.blit(win_sign, (WIDTH/2 - win_width/2, HEIGHT/2))
	if end_timer == 0:
		win_sound.play()
	end_timer += 1
			
	if end_timer >= (FPS * 4):
		RUN = False

#makes enemies to be drawn later
def load_enemies():
	global enemy_list
	enemy = Alien(50, 40)
	for i in range(4):
		for i in range(10):
			enemy = Alien(enemy.x, enemy.y)
			enemy_list.append(enemy)
			enemy.x += enemy_width + 20
		enemy = Alien(50, enemy.y + 50)

#display level screen
def display_new_level(FONT, SCREEN):
	change_level_text = FONT.render(f'LEVEL: {LEVEL}', 1, WHITE)
	change_level_text_width = change_level_text.get_width()
	SCREEN.blit(change_level_text, (WIDTH/2 - change_level_text_width/2, HEIGHT/2))

#load enemy laser to be drawn later
def load_enemy_laser(max_enemy_fire, enemy_list, delta):
	global enemy_laser_list
	temp = random.randint(1, max_enemy_fire)
	enemy_able_to_fire = random.choices(enemy_list, k=temp)[:]	
	enemy_blaster_sound.play()

	for item in enemy_able_to_fire:
		enemy_laser = Laser(item.x + enemy_width/2, item.y + delta + 20)
		enemy_laser_list.append(enemy_laser)


#variables that functions will change
delta = 0
Alien_speed = 1
RUN = True
LEVEL = 0
LIVES = 3
end_timer = 0
enemy_list = []
enemy_laser_list = []

def main():

	global delta
	global Alien_speed
	global RUN 
	global LEVEL
	global LIVES 
	global enemy_list
	global enemy_laser_list

	
	FPS = 60
	
	#1 less than the number of enemies who can initially shoot 
	max_enemy_fire = 1

	#var to disginuish life lost due to alien reaching player
	invade = False

	#player initial position
	player = Ship(WIDTH//2, HEIGHT - player_height)

	#initial conditions for laser
	Laser_fire = False
	laser_list = []
	cooldown = 40

	#var to see if level is changed and timer to count down the display level screen
	level_change = False
	level_timer = 0

	warning_sign(FONT, SCREEN)
	
	
	while RUN:
		
		clock.tick(FPS)
		SCREEN.blit(bg, (0,0))


		#closes tab when x is clicked
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False


		#displaying lives and level
		display_lives_level(FONT, SCREEN)

		#if lives are at 0, display loser for 4 seconds then close the window
		if LIVES <= 0:
			display_loser(END_FONT, SCREEN, FPS)
			pygame.display.update()
			continue

		#if level greater than 6 (level 7), display 'winner' and end game
		if LEVEL > 6:
			display_winner(END_FONT, SCREEN, FPS)
			pygame.display.update()
			continue

		
		#displaying player
		SCREEN.blit(player_image, (player.x, player.y))


		#occurs at the start, after every level, after invasion(enemies reach the player)
		if len(enemy_list) == 0:

			#gain level only if enemy gone due to killing them all, not due to them reaching end of screen
			if invade == False:
				LEVEL += 1
				#level will need to be changed if enemy list is empty not as a result of aliens reaching the player
				level_change = True

				#changes alien speed for each new level
				#must account for if enemies traveling from right to left (thus speed is negative), the speed must increase 
				#by a negative value or else enemy will slow down
				if Alien_speed < 0:
					Alien_speed -= 1
				else:
					Alien_speed += 1
				
				Laser.enemy_fire_speed += 1
				#amount of enemies who can shoot increases each level
				if max_enemy_fire <= 6:
					max_enemy_fire += 1

			#reset values at start of the round
			#remember to reset delta = 0, or else enemies will spawn a row down each level
			invade = False
			delta = 0

			#loads in enemies to enemy list 12 in each row, 5 rows
			load_enemies()

		
		#displays level at the start of the level
		if level_change == True:
			if level_timer <= FPS:
					display_new_level(FONT, SCREEN)
					if level_timer == 0 and LEVEL == 1:
						welcome_sound.play()
					elif level_timer == 0 and LEVEL <= 6:
						level_sound.play()

					level_timer += 1

					pygame.display.update()
					continue
			else:
				level_change = False
				level_timer = 0


		
		#if any aliens on edge, speed becomes negative and delta increases (rows move down)
		edge_check(WIDTH, enemy_list)

		#takes in the list of enemies and displays them
		#delta moves aliens down a row when edge is touched
		#remember that pos of enemy is at self.y + delta 
		for item in enemy_list:
			SCREEN.blit(enemy_image, (item.x, item.y + delta))
			item.x += Alien_speed
			

			#if enemies reach the player, lose a life and enemies are reset without changing level
			#item.y + delta + enemy_height + 30 to make sure enemy is fully within player before invasion happens
			if player.y <= item.y + delta + enemy_height + 30 <= player.y + enemy_height:
				enemy_list = []
				invade = True
				death_sound.play()
		if invade == True:
			LIVES -= 1



		#when the enemy list is empty, pick random eneimies that are able to fire, append laser with that enemy's position to list
		if len(enemy_laser_list) == 0:
			load_enemy_laser(max_enemy_fire, enemy_list, delta)



		#for each enemy in list able to fire, draw laser with speed 3
		for i,laz in enumerate(enemy_laser_list):
			pygame.draw.line(SCREEN, RED, (laz.x, laz.y), (laz.x, laz.y + 20), 3)
			laz.y += Laser.enemy_fire_speed

			#if laser within player, laser removed and lose a life, (laz.y + 13) used instead of (laz.y + 20) to give player leniency
			if player.x <= laz.x <= (player.x + player_width) and player.y <= laz.y + 13 <= (player.y + player_height):
				enemy_laser_list.pop(i)
				LIVES -= 1
				death_sound.play()
			
			#remove laser if out of bounds, using height of last enemy in list and HEIGHT so laser travels same distance even if enemy is closer
			if len(enemy_list) != 0:
				if laz.y >= (enemy_list[-1].y + delta + HEIGHT - 100):
					enemy_laser_list.pop(i)
			else:
				enemy_laser_list.pop(i)

			
		#check if left or right key being pressed and move player accordingly
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and (player.x - player.speed) >= -40:
			player.x -= player.speed
		if keys[pygame.K_RIGHT] and (player.x + player.speed) <= ((WIDTH - player_image.get_width() + 40)):
			player.x += player.speed


		#checks if space pressed, and if so append the laser's position to laser list to be drawn later
		if keys[pygame.K_SPACE] and cooldown >= 40:
			cooldown = 0
			Laser_fire = True
			laser = Laser((player.x + (player_width / 2)), player.y - player_height + 25)
			laser_list.append(laser)
			player_blaster_sound.play()


		#loops through the lasers in laser_list and draws each of them 
		if Laser_fire:
			for i,laz in enumerate(laser_list):
				pygame.draw.line(SCREEN, WHITE, (laz.x, laz.y), (laz.x, laz.y - 15), 2)
				laz.y -= laser.speed


				#Checks for collision, deletes enemy and laser from respective list if laser within enemy
				for j,item in enumerate(enemy_list):
					if item.x <= laz.x <= (item.x + enemy_width) and (item.y + delta) <= laz.y - 15 <= ((item.y + delta) + enemy_height):
						enemy_list.pop(j)
						laser_list.pop(i)

				#removes laser if it goes off screen
				if laz.y >= HEIGHT:
					laser_list.pop(i)


		#cooldown increases per frame, is set to 0 when spacebar is pressed, and spacebar is only allowed to be pressed when cooldown >= 60
		cooldown += 1


			

		pygame.display.update()

if __name__ == '__main__':
	main()

		







