#!/bin/bash

import pygame
from PIL import Image
import json
import traceback
import sys
import copy
import threading

# Constants
SCALER = 4
CHAR_WIDTH = 8
CHAR_HEIGHT = 8
SCREEN_WIDTH = 42
MAX_WIDTH = 40
SCREEN_HEIGHT = 26
MAX_HEIGHT = 25
MAX_LEVELS = 32
fps=10

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

	# Open the WILLY.CHR file
	with open('WILLY.CHR', 'rb') as f:
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

	if len(sys.argv) != 2:
		level=1
	else:
		try:
			level = int(sys.argv[1])
		except:
			level = 1
	
	if level>0 and level <= MAX_LEVELS:
		currentlevel="level" + str(level)
	else:
		currentlevel="level1"

	# Initialize Pygame
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH * CHAR_WIDTH * SCALER, SCREEN_HEIGHT * CHAR_HEIGHT * SCALER))

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


	iterator = iter(font.items())
	currentitem=next(iterator)

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


	for y, x_data in level_data[currentlevel].items():
		if willy_position is not None:
			break
		for x, obj in x_data.items():
			if obj.startswith("WILLY"):
				willy_position = (int(y), int(x))
				willy_object = obj
				break
	level_data[currentlevel][str(willy_position[0])][str(willy_position[1])]="EMPTY"

	clock = pygame.time.Clock()

	while running:
		clock.tick(fps)	 # limit the frame rate to 30 fps
	
		# Handle events
		for event in pygame.event.get():
			# Close Event
			if event.type == pygame.QUIT:
				running = False
			# Keyboard Events
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					willy_yvelocity=3
					print("Spacebar Pressed")
					t = threading.Thread(target=play_audio, args=("audio/jump.wav",))
					t.start()
				elif event.key == pygame.K_LEFT:
					willy_xvelocity=1
					print("Left Key Pressed")
					willy_direction="LEFT"
				elif event.key == pygame.K_RIGHT:
					willy_xvelocity=-1
					print("RIGHT Key Pressed")
					willy_direction="RIGHT"
				elif event.key == pygame.K_UP:
					print("Up Key Pressed")
				elif event.key == pygame.K_DOWN:
					print("Down Key Pressed")
				else:
					print("Any Key Pressed")
					willy_xvelocity=0

			# Right Button Deletes Object
			


		# Clear the screen
		screen.fill((0, 0, 0))

		# Check if there's a PIPE object at Willy's position (below him)
		if willy_position is not None:
			y, x = willy_position
			if not (str(y + 1) in level_data[currentlevel] and str(x) in level_data[currentlevel][str(y + 1)] and level_data[currentlevel][str(y + 1)][str(x)].startswith("PIPE")):
				if willy_yvelocity==0:
					willy_yvelocity = -1
			else:
				if willy_yvelocity<=0:
					willy_yvelocity=0
					
		# If willy is Jumping, check if theres a pipe above him.
		if willy_yvelocity>0:
			if str(y - 1) in level_data[currentlevel] and str(x) in level_data[currentlevel][str(y - 1)] and level_data[currentlevel][str(y - 1)][str(x)].startswith("PIPE"):
				willy_yvelocity=0
		
		if willy_yvelocity>0:
			# Convert tuple to list
			willy_list = list(willy_position)

			# Subtract 1 from the first element of the list
			willy_list[0] -= 1

			# Convert list back to tuple
			willy_position = tuple(willy_list)
			willy_yvelocity-=1

		if willy_yvelocity<0:
			# Convert tuple to list
			willy_list = list(willy_position)

			# Subtract 1 from the first element of the list
			willy_list[0] += 1

			# Convert list back to tuple
			willy_position = tuple(willy_list)

		if willy_xvelocity<0:
			# Convert tuple to list
			willy_list = list(willy_position)

			# Subtract 1 from the first element of the list
			willy_list[1] += 1

			# Convert list back to tuple
			willy_position = tuple(willy_list)

		if willy_xvelocity>0:
			# Convert tuple to list
			willy_list = list(willy_position)

			# Subtract 1 from the first element of the list
			willy_list[1] -= 1

			# Convert list back to tuple
			willy_position = tuple(willy_list)

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

		# Update the screen
		pygame.display.flip()

	# Clean up
	pygame.quit()
	
if __name__ == '__main__':
	main()

