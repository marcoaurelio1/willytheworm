#!/usr/bin/env python

import pygame
from PIL import Image
import json
import traceback
import sys
import threading
import random
import time
import os
from datetime import datetime, date

# Constants
SCALER = 4
CHAR_WIDTH = 8
CHAR_HEIGHT = 8
SCREEN_WIDTH = 40
MAX_WIDTH = 40
SCREEN_HEIGHT = 26
MAX_HEIGHT = 25
MAX_LEVELS = 32
NEWLIFEPOINTS = 2000

# The higher the number, the faster the game goes
fps=10


def game_score(screen, score):
	pygame.display.set_caption('Willy the Worm Game Score')

	font = pygame.font.SysFont("Courier", 32)
	hiscore_msg = ''
	name = ''
	try:
		f=open('willy.scr', 'r+')
		data = f.read()
		hiscores = json.loads(data) 
		#hiscores["hiscoreT"]=[]
		f.close()
		# Get the modification time of the file
		mod_time = os.path.getmtime('willy.scr')

		# Convert the modification time to a datetime object
		mod_datetime = datetime.fromtimestamp(mod_time)

		# Get today's date
		today = date.today()

		# Compare the modification date with today's date
		if not mod_datetime.date() == today:
			hiscores["hiscoreT"]=[]
			
	except:
		hiscores={}
		hiscores["hiscoreT"]=[]
		hiscores["hiscoreP"]=[]
		for x in hiscores:
			for y in range(10):
				hiscores[x].append(("nobody", 0))
				
		pass

	hiscore_msg=""
	if score > hiscores["hiscoreP"][9][1]:
		hiscore_msg = "You're an Official Nightcrawler!"
	elif score > hiscores["hiscoreT"][9][1]:
		hiscore_msg = "You're a Daily Pinworm!"

	score_msg = f"Your score for this game is {score}..."
	if score < 1000:
		score_desc = "Didn't you even read the instructions?"
	elif score < 2000:
		score_desc = "If you can't say anything nice..."
	elif score < 3000:
		score_desc = "Okay. Maybe you're not so bad after all."
	elif score < 4000:
		score_desc = "Wow! Absolutely mediocre!"
	elif score < 5000:
		score_desc = "Pretty darn good, for a vertebrate!"
	elif score < 6000:
		score_desc = "Well done! Do you often eat garbage?"
	else:
		score_desc = "Absolutely fantastic! You should consider a career as an earthworm!"

	messagepointer=0
	incrementer=32
	
	screen.fill((0, 0, 255))
	
	if not hiscore_msg=="":
		message_input_text = font.render(hiscore_msg, False, (255, 255, 255))
		screen.blit(message_input_text, (0, messagepointer))
		messagepointer+=incrementer


	
	message_input_text = font.render(score_desc, False, (255, 255, 255))
	screen.blit(message_input_text, (0, messagepointer))
	messagepointer+=2*incrementer

	message_input_text = font.render("Your score for this game is " + str(score) + "...", False, (255, 255, 255))
	screen.blit(message_input_text, (0, messagepointer))
	messagepointer+=2*incrementer


	pygame.display.update()
	
	for key in hiscores:
		hiscores[key] = sorted(hiscores[key], key=lambda x: x[1], reverse=True)[:10]

	if score > hiscores["hiscoreT"][9][1]:
		#messagepointer+=incrementer


		exittheloop=False
		name_input = ''
		while exittheloop==False:


			messagepointer=0
			if not hiscore_msg=="":
				message_input_text = font.render(hiscore_msg, False, (255, 255, 255))
				screen.blit(message_input_text, (0, messagepointer))
				messagepointer+=incrementer
			
			message_input_text = font.render(score_desc, False, (255, 255, 255))
			screen.blit(message_input_text, (0, messagepointer))
			messagepointer+=2*incrementer

			message_input_text = font.render("Your score for this game is " + str(score) + "...", False, (255, 255, 255))
			screen.blit(message_input_text, (0, messagepointer))
			messagepointer+=2*incrementer

			name_prompt = "Enter your name:"
			message_input_text = font.render("Enter your name >> " + name_input, False, (255, 255, 255))
			screen.blit(message_input_text, (0, messagepointer))


			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					return
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
					if event.key == pygame.K_RETURN:
						name = name_input
						hiscores["hiscoreT"].append([score, name])
						#hiscores["hiscoreT"].sort(reverse=True)
						hiscores["hiscoreT"] = hiscores["hiscoreT"][:10]
						exittheloop=True
						print("Exiting the loop")

					elif event.key == pygame.K_BACKSPACE:
						name_input = name_input[:-1]
						#print("Removing backscape")
						screen.fill((0,0,255)) # clear the screen
					else:
						name_input += event.unicode
				screen.blit(screen, (0,0))
				pygame.display.flip()
				pygame.display.update()
		'''hiscores["hiscoreT"].append((name_input, score))
		#hiscores["hiscoreP"].append((name_input, score))

		for key in hiscores:
			hiscores[key] = sorted(hiscores[key], key=lambda x: x[1], reverse=True)[:10]
			
		print(hiscores)'''
		
		new_data = [name_input, score]

		# Append the new data to the 'hiscoreT' list
		hiscores['hiscoreT'].append(new_data)
		hiscores['hiscoreP'].append(new_data)


		for key in hiscores:
			hiscores[key] = sorted(hiscores[key], key=lambda x: x[1], reverse=True)[:10]

		# Write the updated data back to the file
		with open('willy.scr', 'w') as f:
			json.dump(hiscores, f)
		
		
	else:
		screen.fill((0,0,255)) # clear the screen

		messagepointer=0
		if not hiscore_msg=="":
			message_input_text = font.render(hiscore_msg, False, (255, 255, 255))
			screen.blit(message_input_text, (0, messagepointer))
			messagepointer+=incrementer
			
		message_input_text = font.render(score_desc, False, (255, 255, 255))
		screen.blit(message_input_text, (0, messagepointer))
		messagepointer+=2*incrementer

		message_input_text = font.render("Your score for this game is " + str(score) + "...", False, (255, 255, 255))
		screen.blit(message_input_text, (0, messagepointer))
		messagepointer+=2*incrementer
		
		message_input_text = font.render("Press any key to continue " + str(score) + "...", False, (255, 255, 255))
		screen.blit(message_input_text, (0, messagepointer))
		
		exittheloop=False
		pygame.display.flip()
		pygame.display.update()

		while exittheloop==False:		
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					return
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_F11:
						pygame.display.toggle_fullscreen()
						screen.fill((0, 0, 255))
					elif event.key == pygame.K_ESCAPE:
						print("Goodbye.  Thank you for playing Willy the Worm!!!")
						sys.exit(0)
					else:
						exittheloop=True


	for key in hiscores:
		hiscores[key] = sorted(hiscores[key], key=lambda x: x[1], reverse=True)

	messagepointer=15
	screen.fill((0, 0, 255)) # clear the screen




	# Render the "All-time Nightcrawlers" header
	header_text = font.render("All-time Nightcrawlers", False, (255, 255, 0))
	header_rect = header_text.get_rect(center=(screen.get_width() // 2, messagepointer))
	screen.blit(header_text, header_rect)
	messagepointer+=incrementer

	# Define the dimensions of the table
	table_x = screen.get_width() // 4
	table_y = messagepointer 
	table_width = screen.get_width() // 2
	table_height = incrementer*11

	# Draw a black background for the table
	pygame.draw.rect(screen, (0, 0, 0), (table_x, table_y, table_width, table_height))


	# Render the scores in the table
	for x in range(10):
		formatted_number = '{:2d}'.format(x)
		formatted_score = '{:8d}'.format(hiscores["hiscoreP"][x][1])
		username=hiscores["hiscoreP"][x][0]
		message_input_text = font.render(formatted_number + "     " + formatted_score + "     " + username, False, (255, 255, 0))
		
		screen.blit(message_input_text, (table_x+10, messagepointer))
		messagepointer+=incrementer

	messagepointer+=2*incrementer


	# Render the "All-time Nightcrawlers" header
	header_text = font.render("Today's Best Pinworms", False, (0, 255, 255))
	header_rect = header_text.get_rect(center=(screen.get_width() // 2, messagepointer))
	screen.blit(header_text, header_rect)

	# Define the dimensions of the table
	table_x = screen.get_width() // 4
	table_y = messagepointer + table_y-16
	table_width = screen.get_width() // 2
	table_height = incrementer*11

	messagepointer+=incrementer

	# Draw a black background for the table
	pygame.draw.rect(screen, (0, 0, 0), (table_x, table_y, table_width, table_height))


	# Render the scores in the table
	for x in range(10):
		formatted_number = '{:2d}'.format(x)
		formatted_score = '{:8d}'.format(hiscores["hiscoreT"][x][1])
		username=hiscores["hiscoreT"][x][0]
		message_input_text = font.render(formatted_number + "     " + formatted_score + "     " + username, False, (0, 255, 255))
		
		screen.blit(message_input_text, (table_x+10, messagepointer))
		messagepointer+=incrementer

	messagepointer+=incrementer*2

	header_text = font.render("Hit any key to play again or ESC to exit", False, (255, 255, 255))
	header_rect = header_text.get_rect(center=(screen.get_width() // 2, messagepointer))
	screen.blit(header_text, header_rect)


	pygame.display.flip()
	pygame.display.update()

	exittheloop=False
	
	while exittheloop==False:		

		
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				pygame.quit()
				return
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
				else:
					exittheloop=True

	
	
	

def deadscreen(screen, score):
	screen.fill((0, 0, 255))
	exit=False
	while exit==False:
		datasize=0
		screenwidth=SCREEN_WIDTH * CHAR_WIDTH * SCALER
		font_size = 8*SCALER
		fontdata = pygame.font.SysFont(None, font_size)
		# Render the text as a surface
		text = "You have died"
		#text = "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789"
		text_surface = fontdata.render(text, True, (255, 255, 255))
		text_rect = text_surface.get_rect()
		text_x = (screenwidth - text_rect.width) // 2
		#text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - font_size
		text_y = 0
		screen.blit(text_surface, (text_x, text_y))

		text = "When you died, you had " + str(score) + " points."
		spaces=int((datasize-len(text))/2)
		text_surface = fontdata.render(text, True, (255, 255, 255))
		text_rect = text_surface.get_rect()
		text_x = (screenwidth - text_rect.width) // 2
		#text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - font_size
		text_y = font_size+2
		screen.blit(text_surface, (text_x, text_y))

		text = "Press Enter to Continue"
		spaces=int((datasize-len(text))/2)
		text_surface = fontdata.render(text, True, (255, 255, 255))
		text_rect = text_surface.get_rect()
		text_x = (screenwidth - text_rect.width) // 2
		#text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - font_size
		text_y = 4*font_size+2
		screen.blit(text_surface, (text_x, text_y))



		pygame.display.flip()
		for event in pygame.event.get():
			# Keyboard Events
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					exit=True



def intro(screen):

	screen.fill((0, 0, 255))
	exit=False
	willyfont=loadFont()
	while exit==False:
		datasize=0
		screenwidth=SCREEN_WIDTH * CHAR_WIDTH * SCALER
		font_size = 32
		fontdata = pygame.font.SysFont("Courier", font_size)
		# Render the text as a surface

		textdata=[["Willy the Worm"],
		[""],
		["By Jason Hall"], 
		["(original version by Alan Farmer 1985)"],
		[""],
		["This code is Free Open Source Software (FOSS)"],
		["Please feel free to do with it whatever you wish."],
		[""], 
		["If you do make changes though such as new levels,"],
		["please share them with the world."],
		[""], 
		[""],
		["Meet Willy the Worm ", "WILLY_RIGHT", ". Willy is a fun-"],
		["loving invertebrate who likes to climb"],
		["ladders ", "LADDER", " bounce on springs ", "UPSPRING", " ", "SIDESPRING"],
		["and find his presents ", "PRESENT", ".  But more"],
		["than anything, Willy loves to ring,"],
		["bells! ", "BELL"],
		[""],
		["You can press the arrow keys ↤ ↥ ↦ ↧"],
		["to make Willy run and climb, or the"],
		["space bar to make him jump. Anything"],
		["else will make Willy stop and wait"],
		[""],
		["Good luck, and don't let Willy step on"],
		["a tack! ", "TACK"],
		[""],
		["Press Enter to Continue"]]

		screenwidth=SCREEN_WIDTH * CHAR_WIDTH * SCALER
		font_size = 8*SCALER
		fontdata = pygame.font.SysFont("Courier", font_size)
		# Render the text as a surface
		counter=0
		namer=0
		for message in textdata:
			max_width=0
			currentpos=0
			for message2 in message:
				if not willyfont.get(message2)==None:
					max_width+=8*SCALER
				else:
					text_surface = fontdata.render(message2, False, (255, 255, 255))
					text_rect = text_surface.get_rect()
					max_width+=text_rect.width

			for message2 in message:
				if not willyfont.get(message2)==None:
					text_surface = willyfont[message2]
					#text_rect = text_surface.get_rect()
					if currentpos==0:
						currentpos = (screenwidth - max_width) // 2
					screen.blit(text_surface, (currentpos, font_size*counter+2))
					currentpos+=8*SCALER
				else:
					text_surface = fontdata.render(message2, False, (255, 255, 255))
					text_rect = text_surface.get_rect()
					if currentpos==0:
						currentpos = (screenwidth - max_width) // 2
					screen.blit(text_surface, (currentpos, font_size*counter+2))
					currentpos+=text_rect.width

			counter+=1



			'''
			text_surface = fontdata.render(text.replace("\n", ""), True, (255, 255, 255))
			text_rect = text_surface.get_rect()
			text_x = (screenwidth - text_rect.width) // 2
			text_y = (counter*font_size)+2
			screen.blit(text_surface, (text_x, text_y))
			namer+=1
			if "\n" in text:
				counter+=1'''
			



		#col = 0
		#row = 0
		#screen.blit(char_img, (int(col) * CHAR_WIDTH * SCALER, int(row) * CHAR_HEIGHT * SCALER))
		#screen.blit(char_img, (int(col) * CHAR_WIDTH * SCALER, int(row) * CHAR_HEIGHT * SCALER))

		# Calculate the number of characters that fit horizontally and vertically in the window


		pygame.display.flip()
		for event in pygame.event.get():
			# Keyboard Events
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					exit=True
				if event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()
					screen.fill((0, 0, 255))

				if event.key == pygame.K_ESCAPE:
					print("Goodbye.  Thank you for playing Willy the Worm!!!")
					sys.exit(0)


def play_audio(filename):
	pygame.mixer.init()
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play()
	
def loadFont():

	namedpart={}
	namedpart["0"]="WILLY_RIGHT"
	namedpart["1"]="WILLY_LEFT"
	namedpart["2"]="PRESENT"
	namedpart["3"]="LADDER"
	namedpart["4"]="TACK"
	namedpart["5"]="UPSPRING"
	namedpart["6"]="SIDESPRING"
	namedpart["7"]="BALL"
	namedpart["8"]="BELL"
	namedpart["51"]="PIPE1"
	namedpart["52"]="PIPE2"
	namedpart["53"]="PIPE3"
	namedpart["54"]="PIPE4"
	namedpart["55"]="PIPE5"
	namedpart["56"]="PIPE6"
	namedpart["57"]="PIPE7"
	namedpart["58"]="PIPE8"
	namedpart["59"]="PIPE9"
	namedpart["60"]="PIPE10"
	namedpart["61"]="PIPE11"
	namedpart["62"]="PIPE12"
	namedpart["63"]="PIPE13"
	namedpart["64"]="PIPE14"
	namedpart["65"]="PIPE15"
	namedpart["66"]="PIPE16"
	namedpart["67"]="PIPE17"
	# Destroyable
	namedpart["68"]="PIPE18"
	namedpart["69"]="PIPE19"
	namedpart["70"]="PIPE20"
	namedpart["71"]="PIPE21"
	namedpart["72"]="PIPE22"
	namedpart["73"]="PIPE23"
	namedpart["74"]="PIPE24"
	namedpart["75"]="PIPE25"
	namedpart["76"]="PIPE26"
	namedpart["77"]="PIPE27"
	namedpart["78"]="PIPE28"
	namedpart["79"]="PIPE29"
	namedpart["80"]="PIPE30"
	namedpart["81"]="PIPE31"
	namedpart["82"]="PIPE32"
	namedpart["83"]="PIPE33"
	namedpart["84"]="PIPE34"
	namedpart["85"]="PIPE35"
	namedpart["86"]="PIPE36"
	namedpart["87"]="PIPE37"
	namedpart["88"]="PIPE38"
	namedpart["89"]="PIPE39"
	namedpart["90"]="PIPE40"
	namedpart["126"]="BALLPIT"
	namedpart["127"]="EMPTY"
	

	# Define the colors (in RGB format)
	BACKGROUND = (0, 0, 255)
	WHITE = (255, 255, 255)

	# Define the size of the output image (in pixels)
	IMAGE_WIDTH = 128
	IMAGE_HEIGHT = 256

	# Open the willy.chr file
	with open('willy.chr', 'rb') as f:
		# Read the file contents into a bytearray
		data = bytearray(f.read())

	# Create a new PIL image
	img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND)

	char_array={}

	counter=0
	# Loop through the characters in the file
	for i in range(len(data) // 8):
		# Extract the bits for each row of the character
		bits = [((data[i * 8 + j] >> k) & 1) for j in range(8) for k in range(7, -1, -1)]
		
		# Create a new PIL image for the character
		char_img = Image.new('RGB', (CHAR_WIDTH, CHAR_HEIGHT), BACKGROUND)
		# Loop through the rows of the character
		for y in range(CHAR_HEIGHT):
			# Loop through the pixels in the row
			for x in range(CHAR_WIDTH):
				# Calculate the index of the pixel in the bits array
				index = y * CHAR_WIDTH + x
				
				# If the bit is set, set the pixel to white
				if bits[index] == 1:
					char_img.putpixel((x, y), WHITE)

		new_size = (char_img.size[0] * SCALER, char_img.size[1] * SCALER)
		char_img = char_img.resize(new_size)
		pygame_image = pygame.image.fromstring(char_img.tobytes(), char_img.size, char_img.mode).convert()
		try:
			partnumber=namedpart[str(counter)]
			char_array[partnumber]=pygame_image
		except:
			#char_array[str(counter)]=pygame_image
			pass
		counter+=1

	return char_array

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH * CHAR_WIDTH * SCALER, SCREEN_HEIGHT * CHAR_HEIGHT * SCALER), pygame.FULLSCREEN)
	wasd=False
	level=1
	i = 1
	while i < len(sys.argv):
		arg = sys.argv[i]
		if arg == "-l" and i + 1 < len(sys.argv):
			try:
				level = int(sys.argv[i + 1])
			except ValueError:
				print("Invalid argument for -l")
				sys.exit(1)
			i += 1
		elif arg == "-w":
			wasd = True
		else:
			print("Unknown argument:", arg)
			sys.exit(1)
		i += 1
		

	intro(screen)
	while True:
		if level>0 and level <= MAX_LEVELS:
			currentlevel="level" + str(level)
		else:
			currentlevel="level1"

		score=game(screen, currentlevel, level, wasd)
		game_score(screen, score)
		level=1


def game(screen, currentlevel, level, wasd=False):


	# Initialize Pygame
	# Load the font
	font = loadFont()


	# Create a 2D array to store the level data
	#level_data = [[None] * SCREEN_WIDTH for i in range(SCREEN_HEIGHT)]
	# Create a 2D array to store the level data
	#level_data = {}
	#level_data[currentlevel]={}


	try:
		with open('levels.json', 'r') as file:
			# Load the data from the file using the json.load() function
			level_data = json.load(file)
	except:
		traceback.print_exc()
		print("Can't load levels.json; starting over")
		sys.exit()


	#iterator = iter(font.items())
	#currentitem=next(iterator)

	# Game loop
	running = True

	row = 0
	col = SCREEN_WIDTH-1
	#level_data[row][col] = font["WILLY_RIGHT"]
	if level_data.get(currentlevel)==None:
		#level_data[curentlevel]={}
		level_data[currentlevel]={}
	for row in range(SCREEN_HEIGHT):
		if level_data.get(currentlevel).get(str(row))==None:
			level_data[currentlevel][str(row)]={}
		for col in range(SCREEN_WIDTH):
			if level_data[currentlevel].get(str(row)).get(str(col))==None:
				level_data[currentlevel][str(row)][str(col)]="EMPTY"

	willy_position = None
	willy_object = None
	willy_yvelocity = 0
	willy_xvelocity = 0
	willy_direction = None
	ladder_direction = None
	score=0
	bonus=1000
	numberoflives=5
	numberofballs=6
	ballkilledwilly=False

	for y, x_data in level_data[currentlevel].items():
		if willy_position is not None:
			break
		for x, obj in x_data.items():
			if obj.startswith("WILLY"):
				willy_position = (int(y), int(x))
				willy_object = obj
				break
	level_data[currentlevel][str(willy_position[0])][str(willy_position[1])]="EMPTY"

	init_position=willy_position
	
	clock = pygame.time.Clock()

	# Used for bonuses
	fpscounter=0

	primaryballpit=level_data.get(currentlevel+"PIT").get("PRIMARYBALLPIT")

	balls={}
	counter=0
	for ball in range(numberofballs):
		balls[str(counter)] = {}
		balls[str(counter)]["Location"] = [primaryballpit[0], primaryballpit[1]]
		balls[str(counter)]["Direction"] = None
		counter += 1
	liveadder=0

	while running:
		clock.tick(fps)	 # limit the frame rate to 30 fps
		if int(score/NEWLIFEPOINTS)>liveadder:
			numberoflives+=1
			liveadder+=1
		'''
		# Handle events
		mouse_movement = pygame.mouse.get_rel()
		
		print("Mouse Movement", mouse_movement)
		if mouse_movement[0] < 0:
			willy_xvelocity=1
			#print("Left Key Pressed")
			willy_direction="LEFT"
			ladder_direction="LEFT"
		elif mouse_movement[0] > 0:
			willy_xvelocity=-1
			#print("RIGHT Key Pressed")
			willy_direction="RIGHT"
			ladder_direction="RIGHT"'''		
		for event in pygame.event.get():
			# Close Event
			if event.type == pygame.QUIT:
				running = False
			# Keyboard Events
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					print("Goodbye.  Thank you for playing Willy the Worm!!!")
					sys.exit(0)
				if event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()
				#if event.key == pygame.K_SPACE or (event.type == pygame.MOUSEBUTTONDOWN and event.button==1):
				if event.key == pygame.K_SPACE:
					y,x = willy_position
					if (willy_yvelocity==0 and level_data[currentlevel][str(y + 1)][str(x)].startswith("PIPE")) or y==(MAX_HEIGHT-1):
						willy_yvelocity=4
						#print("Spacebar Pressed")
						t = threading.Thread(target=play_audio, args=("audio/jump.mp3",))
						t.start()
				elif (event.key == pygame.K_LEFT and wasd==False) or (event.key == pygame.K_a and wasd==True):
					willy_xvelocity=1
					#print("Left Key Pressed")
					willy_direction="LEFT"
					ladder_direction="LEFT"

				elif (event.key == pygame.K_RIGHT and wasd==False) or (event.key == pygame.K_d and wasd==True):
					willy_xvelocity=-1
					#print("RIGHT Key Pressed")
					willy_direction="RIGHT"
					ladder_direction="RIGHT"
				#elif event.key == pygame.K_UP or event.key == pygame.K_w or (event.type == pygame.MOUSEBUTTONDOWN and event.button==3):
				elif (event.key == pygame.K_UP and wasd==False) or (event.key == pygame.K_w and wasd==True):
					#print("Up Key Pressed")
					ladder_direction="UP"
				#elif event.key == pygame.K_DOWN or event.key == pygame.K_s or (event.type == pygame.MOUSEBUTTONDOWN and event.button==2):
				elif (event.key == pygame.K_DOWN and wasd==False) or (event.key == pygame.K_s and wasd==True):
					#print("Down Key Pressed")
					ladder_direction="DOWN"
				else:
					#print("Any Key Pressed")
					willy_xvelocity=0
					ladder_direction=None


			# Right Button Deletes Object
			


		# Clear the screen
		screen.fill((0, 0, 0))

		# Check if there's a PIPE object at Willy's position (below him)
		if willy_position is not None:
			y, x = willy_position
			if not (str(y + 1) in level_data[currentlevel] and str(x) in level_data[currentlevel][str(y + 1)] and level_data[currentlevel][str(y + 1)][str(x)].startswith("PIPE")):
				if willy_yvelocity==0 and not (level_data[currentlevel][str(y)][str(x)].startswith("LADDER") or level_data[currentlevel][str(y+1)][str(x)].startswith("LADDER")):
					willy_yvelocity = -1
			else:
				if willy_yvelocity<=0:
					willy_yvelocity=0

		for ball in balls:
			#print(balls[ball])
			col=balls[ball]["Location"][1]
			row=balls[ball]["Location"][0]
			willyrow, willycol = willy_position
			if willyrow==row and willycol==col and not level_data[currentlevel][str(row)][str(col)].startswith("BALLPIT"):
				ballkilledwilly=True
		
		if level_data[currentlevel][str(willy_position[0]+1)][str(willy_position[1])].startswith("PIPE18"):
			level_data[currentlevel][str(willy_position[0]+1)][str(willy_position[1])]="EMPTY"
		
		if level_data[currentlevel][str(willy_position[0])][str(willy_position[1])].startswith("TACK") or bonus<=0 or ballkilledwilly==True or level_data[currentlevel][str(willy_position[0])][str(willy_position[1])].startswith("BELL"):
			ballkilledwilly=False
			if not level_data[currentlevel][str(willy_position[0])][str(willy_position[1])].startswith("BELL"):
				with open('levels.json', 'r') as file:
					# Load the data from the file using the json.load() function
					level_data = json.load(file)


				t = threading.Thread(target=play_audio, args=("audio/tack.mp3",))
				t.start()
				numberoflives-=1
				color1 = (255, 255, 255)
				color2 = (255, 255, 255)

				# Calculate the duration of the flashing in seconds
				duration = 0.25

				# Calculate the number of times to switch between colors
				num_flashes = int(duration * 60) # assuming a 60 FPS refresh rate

				# Start the flashing
				for i in range(num_flashes):
					# Alternate between the two colors
					if i % 2 == 0:
						screen.fill(color1)
					else:
						screen.fill(color2)
					
					# Update the display
					pygame.display.update()
					
					# Wait for a short amount of time before the next frame
					time.sleep(1/60)


			else:
				with open('levels.json', 'r') as file:
					# Load the data from the file using the json.load() function
					level_data = json.load(file)
				t = threading.Thread(target=play_audio, args=("audio/bell.mp3",))
				t.start()
				level+=1
				score+=bonus
				if level>MAX_LEVELS:
					level=1
				currentlevel="level" + str(level)
				if level_data.get(currentlevel)==None:
					#level_data[curentlevel]={}
					level_data[currentlevel]={}
			for row in range(SCREEN_HEIGHT):
				if level_data.get(currentlevel).get(str(row))==None:
					level_data[currentlevel][str(row)]={}
				for col in range(SCREEN_WIDTH):
					if level_data[currentlevel].get(str(row)).get(str(col))==None:
						level_data[currentlevel][str(row)][str(col)]="EMPTY"

			willy_position = None
			willy_object = None
			willy_yvelocity = 0
			willy_xvelocity = 0
			willy_direction = None
			ladder_direction = None
			bonus=1000
			fpscounter=0

			for y, x_data in level_data[currentlevel].items():
				if willy_position is not None:
					break
				for x, obj in x_data.items():
					if obj.startswith("WILLY"):
						willy_position = (int(y), int(x))
						willy_object = obj
						break
			level_data[currentlevel][str(willy_position[0])][str(willy_position[1])]="EMPTY"
			init_position=willy_position
			willy_position=init_position
			primaryballpit=level_data.get(currentlevel+"PIT").get("PRIMARYBALLPIT")



			
			if numberoflives<1:
				# Todo; make main screen
				return score
			else:
				if level_data.get(currentlevel)==None:
					#level_data[curentlevel]={}
					level_data[currentlevel]={}
				for row in range(SCREEN_HEIGHT):
					if level_data.get(currentlevel).get(str(row))==None:
						level_data[currentlevel][str(row)]={}
					for col in range(SCREEN_WIDTH):
						if level_data[currentlevel].get(str(row)).get(str(col))==None:
							level_data[currentlevel][str(row)][str(col)]="EMPTY"

			balls={}
			counter=0
			for ball in range(numberofballs):
				balls[str(counter)] = {}
				balls[str(counter)]["Location"] = [primaryballpit[0], primaryballpit[1]]
				balls[str(counter)]["Direction"] = None
				counter += 1			


		'''if level_data[currentlevel][str(willy_position[0])][str(willy_position[1])].startswith("LADDER") and ladder_direction==None:
			willy_yvelocity=0
			willy_xvelocity=0'''		

		willy_list = list(willy_position)
		if level_data[currentlevel][str(willy_list[0]+1)][str(willy_list[1])].startswith("LADDER") and level_data[currentlevel][str(willy_list[0])][str(willy_list[1])].startswith("EMPTY"):
			willy_yvelocity=-1


		if level_data[currentlevel][str(willy_position[0])][str(willy_position[1])].startswith("UPSPRING"):
			willy_yvelocity=4
			t = threading.Thread(target=play_audio, args=("audio/jump.mp3",))
			t.start()

		if level_data[currentlevel][str(willy_position[0])][str(willy_position[1])].startswith("SIDESPRING"):
			willy_xvelocity*=-1
			t = threading.Thread(target=play_audio, args=("audio/jump.mp3",))
			t.start()
			if willy_direction=="LEFT":
				willy_direction="RIGHT"
			else:
				willy_direction="LEFT"


		if level_data[currentlevel][str(willy_position[0])][str(willy_position[1])].startswith("PRESENT"):
			score+=100
			t = threading.Thread(target=play_audio, args=("audio/present.mp3",))
			t.start()
			level_data[currentlevel][str(willy_position[0])][str(willy_position[1])]="EMPTY"


		# If willy is Jumping, check if theres a pipe beside him.
		if willy_xvelocity>0:
			if str(y) in level_data[currentlevel] and str(x - 1) in level_data[currentlevel][str(y)] and level_data[currentlevel][str(y)][str(x - 1)].startswith("PIPE"):
				willy_xvelocity=0

		if willy_xvelocity<0:
			if str(y) in level_data[currentlevel] and str(x + 1) in level_data[currentlevel][str(y)] and level_data[currentlevel][str(y)][str(x + 1)].startswith("PIPE"):
				willy_xvelocity=0


		if willy_yvelocity>0:
			if str(y - 1) in level_data[currentlevel] and str(x) in level_data[currentlevel][str(y - 1)] and level_data[currentlevel][str(y - 1)][str(x)].startswith("PIPE"):
				willy_yvelocity=0
		
		
		if willy_yvelocity>0:
			# Convert tuple to list
			willy_list = list(willy_position)

			# Create a new list with the same values as willy_list
			test_list = [elem for elem in willy_list]

			# Subtract 1 from the first element of the list
			if test_list[0] > 0:
				test_list[0] -= 1

			if not level_data[currentlevel][str(test_list[0])][str(test_list[1])].startswith("PIPE"):
				willy_list = [elem for elem in test_list]

			# Delete the test_list variable
			del test_list

			# Convert list back to tuple
			willy_position = tuple(willy_list)
			willy_yvelocity -= 1

		if willy_yvelocity<0:
			# Convert tuple to list
			willy_list = list(willy_position)

			# Create a new list with the same values as willy_list
			test_list = [elem for elem in willy_list]

			# Subtract 1 from the first element of the list
			if test_list[0] < (MAX_HEIGHT - 1):
				test_list[0] += 1

			if not level_data[currentlevel][str(test_list[0])][str(test_list[1])].startswith("PIPE"):
				willy_list = test_list

			# Delete the test_list variable
			del test_list

			# Convert list back to tuple
			willy_position = tuple(willy_list)

		if willy_xvelocity<0:
			# Convert tuple to list
			willy_list = list(willy_position)
			test_list = [elem for elem in willy_list]


			# Subtract 1 from the first element of the list
			if test_list[1]<(MAX_WIDTH-1):
				test_list[1] += 1

			if not level_data[currentlevel][str(test_list[0])][str(test_list[1])].startswith("PIPE"):
				willy_list=test_list
			del test_list
	
			# Convert list back to tuple
			willy_position = tuple(willy_list)

		if willy_xvelocity>0:
			# Convert tuple to list
			willy_list = list(willy_position)
			test_list = [elem for elem in willy_list]

			# Subtract 1 from the first element of the list
			if test_list[1]>0:
				test_list[1] -= 1

			if not level_data[currentlevel][str(test_list[0])][str(test_list[1])].startswith("PIPE"):
				willy_list=test_list


			del test_list
								
			# Convert list back to tuple
			willy_position = tuple(willy_list)

		willy_list = list(willy_position)
		if ladder_direction=="UP" and level_data[currentlevel][str(willy_list[0])][str(willy_list[1])].startswith("LADDER"):
			#print("Going up Ladder")
			# Convert tuple to list
			willy_list = list(willy_position)
			test_list=[elem for elem in willy_list]
			# Subtract 1 from the first element of the list
			if test_list[0]>0:
				test_list[0] -= 1

			if level_data[currentlevel][str(test_list[0])][str(test_list[1])].startswith("LADDER"):
				willy_list=test_list
				
			del test_list

			# Convert list back to tuple
			willy_position = tuple(willy_list)
			willy_xvelocity=0
			willy_yvelocity=0
			t = threading.Thread(target=play_audio, args=("audio/ladder.mp3",))
			t.start()

		willy_list = list(willy_position)
		if ladder_direction=="DOWN" and level_data[currentlevel][str(willy_list[0])][str(willy_list[1])].startswith("LADDER"):
			# Convert tuple to list
			willy_xvelocity=-1
			willy_list = list(willy_position)
			test_list=[elem for elem in willy_list]
			# Subtract 1 from the first element of the list
			if test_list[0]<(MAX_HEIGHT-1):
				test_list[0] += 1

			if level_data[currentlevel][str(test_list[0])][str(test_list[1])].startswith("LADDER") or level_data[currentlevel][str(test_list[0])][str(test_list[1])].startswith("EMPTY"):
				willy_list=test_list
			del test_list

				
			# Convert list back to tuple
			willy_position = tuple(willy_list)
			willy_xvelocity=0
			willy_yvelocity=0
			t = threading.Thread(target=play_audio, args=("audio/ladder.mp3",))
			t.start()

		for ball in balls:
			#print(balls[ball])
			col=balls[ball]["Location"][1]
			row=balls[ball]["Location"][0]
			willyrow, willycol = willy_position
			if willyrow==row and willycol==col and not level_data[currentlevel][str(row)][str(col)].startswith("BALLPIT"):
				ballkilledwilly=True


		for row in level_data[currentlevel]:
			for col in level_data[currentlevel][row]:
				char_img = font[level_data[currentlevel][row][col]]
				screen.blit(char_img, (int(col) * CHAR_WIDTH * SCALER, int(row) * CHAR_HEIGHT * SCALER))
				#print(char_img)	
		
		#print(willy_direction)
		if willy_direction=="LEFT":
			char_img = font["WILLY_LEFT"]
		else:
			char_img = font["WILLY_RIGHT"]	
		row, col = willy_position
		screen.blit(char_img, (int(col) * CHAR_WIDTH * SCALER, int(row) * CHAR_HEIGHT * SCALER))

		font_size = 8*SCALER
		fontdata = pygame.font.SysFont(None, font_size)


		for ball in balls:
			#print(balls[ball])
			col=balls[ball]["Location"][1]
			row=balls[ball]["Location"][0]
			
			if level_data[currentlevel][str(row)][str(col)].startswith("BALLPIT"):
				if not (balls[ball]["Location"][1]==primaryballpit[1] and balls[ball]["Location"][0]==primaryballpit[0]):
					balls[ball]["Location"][1]=primaryballpit[1]
					balls[ball]["Location"][0]=primaryballpit[0]
					balls[ball]["Direction"]==None
					col=balls[ball]["Location"][1]
					row=balls[ball]["Location"][0]
			if not level_data[currentlevel][str(row+1)][str(col)].startswith("PIPE") and row<(MAX_HEIGHT-1):
				if col==primaryballpit[1] and row==primaryballpit[0]:
					data=random.randint(0,40)
				else:
					data=0
				if data==0:
					balls[ball]["Location"][0]+=1
					balls[ball]["Direction"]=None
			else:
				if balls[ball]["Direction"]==None:
					data=random.randint(0,1)
					if data==0:
						balls[ball]["Direction"]="RIGHT"
					else:
						balls[ball]["Direction"]="LEFT"
					
					'''	if (col+1)<MAX_WIDTH and not level_data[currentlevel][str(row)][str(col+1)].startswith("PIPE"):
							balls[ball]["Location"][1]+=1
							balls[ball]["Direction"]="RIGHT"
						else:
							balls[ball]["Direction"]="LEFT"
					else:
						if (col-1)>=0 and not level_data[currentlevel][str(row)][str(col-1)].startswith("PIPE"):
							balls[ball]["Location"][1]-=1
							balls[ball]["Direction"]="LEFT"
						else:
							balls[ball]["Direction"]="RIGHT"'''
				if balls[ball]["Direction"]=="RIGHT":
					if (balls[ball]["Location"][1]+1)<(MAX_WIDTH) and (col+1)<MAX_WIDTH and not level_data[currentlevel][str(row)][str(col+1)].startswith("PIPE"):
						balls[ball]["Location"][1]+=1
					else:
						balls[ball]["Direction"]="LEFT"
				else:
					if (balls[ball]["Location"][1]-1)>=0 and not level_data[currentlevel][str(row)][str(col-1)].startswith("PIPE"):
						balls[ball]["Location"][1]-=1
					else:
						balls[ball]["Direction"]="RIGHT"						
			char_img = font["BALL"]
			if not level_data[currentlevel][str(row)][str(col)].startswith("BALLPIT"):
				screen.blit(char_img, (int(col) * CHAR_WIDTH * SCALER, int(row) * CHAR_HEIGHT * SCALER))
		
		for ball in balls:
			#print(balls[ball])
			col=balls[ball]["Location"][1]
			row=balls[ball]["Location"][0]
			willyrow, willycol = willy_position
			if willyrow==row and willycol==col and not level_data[currentlevel][str(row)][str(col)].startswith("BALLPIT"):
				ballkilledwilly=True
			y, x = willy_position
			for i in range(1, 5):
				if str(y + i) in level_data[currentlevel] and str(x) in level_data[currentlevel][str(y + i)] and (y+i)==row and x==col and willy_yvelocity>0:
					# Add 20 points to Willy's score here
					score+=20
					t = threading.Thread(target=play_audio, args=("audio/boop.mp3",))
					t.start()
					break
		
		
		# Render the text as a surface
		text = "SCORE: " + str(score)
		text_surface = fontdata.render(text, True, (255, 255, 255))

		# Blit the text surface onto the screen at a specific location
		#text_x = (SCREEN_WIDTH * CHAR_WIDTH * SCALER)-10
		#text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - 10 
		text_x = 25*SCALER
		text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - font_size
		#print(SCREEN_WIDTH * CHAR_WIDTH * SCALER, SCREEN_HEIGHT * CHAR_HEIGHT * SCALER)
		screen.blit(text_surface, (text_x, text_y))

		# Render the text as a surface
		text = "BONUS: " + str(bonus)
		text_surface = fontdata.render(text, True, (255, 255, 255))

		text_x = 4*25*SCALER
		text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - font_size
		screen.blit(text_surface, (text_x, text_y))
		fpscounter+=1
		if fpscounter>=fps:
			fpscounter=0
			bonus-=10

		# Render the text as a surface
		text = "Level: " + str(level)
		text_surface = fontdata.render(text, True, (255, 255, 255))

		text_x = 6*25*SCALER
		text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - font_size
		screen.blit(text_surface, (text_x, text_y))


		# Render the text as a surface
		text = "Willy the Worms Left: " + str(numberoflives)
		text_surface = fontdata.render(text, True, (255, 255, 255))

		text_x = 8*25*SCALER
		text_y = (SCREEN_HEIGHT * CHAR_HEIGHT * SCALER) - font_size
		screen.blit(text_surface, (text_x, text_y))


		# Update the screen
		pygame.display.flip()

	# Clean up
	pygame.quit()
	
if __name__ == '__main__':
	main()

