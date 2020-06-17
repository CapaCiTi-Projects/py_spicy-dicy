import random
import re
import sys
import time

__consts__ = {
	"name": "Spicy Dicy",
	"version": "0.9.0b",
	"author": "Jesse Boise",
	"year": "2020",
	"copyright": "Copyright \u00a9 {} {}"
}
__consts__['copyright'] = __consts__['copyright'].format(__consts__['author'], __consts__['year'])

class Die:
	"""Class that represents a single die."""
	__die_grid = [
		[ [2, 3, 4, 5, 6, 7, 8, 9], [9], [4, 5, 6, 7, 8, 9] ],
		[ [6, 7, 8, 9], [1, 3, 5, 7, 9], [6, 7, 8, 9] ],
		[ [4, 5, 6, 7, 8, 9], [9], [2, 3, 4, 5, 6, 7, 8, 9] ]
	]

	def __init__(self, faces):
		"""Initialise the die with the supplied number of faces / sides and then perform a die roll, so that Die is initialised with a base random value."""
		self.faces = faces
		self.face = -1

		self.roll()
	
	def roll(self):
		"""Calculate a pseudo-random number using the random module and set the class variable `face` to it."""
		val = random.randrange(1, self.faces + 1)
		self.face = val
		return val

	def get_faces(self):
		"""Get the current number of faces of the die."""
		return self.faces

	def draw_text(self):
		"""Convert the die into a string picture using unicode characters."""
		grid = ''

		# Loop through the die grid, if the current face is in the list at the row and column of the die grid,
		# then add a circle (`\u2299`), otherwise add a space(`\u0020`).
		for row in Die.__die_grid:
			for col in row:
				if self.face in col:
					grid += '\u2299'
				else:
					grid += '\u0020'
			grid += '\n'
		grid += '\u0020' + str(self.face) + '\u0020'

		return grid

def merge_dice_text(dice):
	"""Function to take all of the supplied die's, and draw them next to each other. To do this, I have created a list list called lines which stores each line to be displayed. The program adds each line from each die to their required line in the lines list and then adds a tab to create spacing between the elements. lines thus becomes a list containing lists of all of the lines of the output which gets converted into text and then is returned."""
	lines = [[], [], [], []] # always 4 lines for drawing

	for idx in range(len(dice)): # loop through each die object
		die = dice[idx].draw_text() # get the text to be drawn for this die
		die_lines = die.split("\n")[:4] #  ensures that a max of 4 lines are used

		for line in range(0, 4): # loop through each line in the die
			lines[line] += die_lines[line] + '\t' # add the current line to the proper line in the lines list

	out = ''
	for idx in range(len(lines)):
		line = lines[idx]

		if idx == 3:
			out += '\n' # adds a space before displaying the number character that is in this die, to make it easier to read.
		out += ''.join(line) # join the line from the lines list spaces
		out += '\n' # each line is drawn on a new line, so add a newline to indicate this

	return out

def print_animated(out, delay):
	for line in out:
		for c in line:
			sys.stdout.write(c)
			sys.stdout.flush()

			time.sleep(delay)
	print('')

def get_first_int(val, default):
	"""Function to see if the supplied val is an integer or starts with an integer, if so return that integer, otherwise return default."""
	match = re.search("^\d+", val)
	return int(match.group()) if match is not None else default

def get_yes_no_bool(val, default=False):
	val = val.lower()
	if val.startswith('yes') or val == 'y':
		return True
	elif val.startswith('no') or val == 'n':
		return False
	else:
		return default

if __name__ == '__main__':
	# Only run the following code if this isn't being run as a module.
	intro_image = (
		r"     ____             " + "\n" +
		r"    /\' .\    _____   " + "\n" +
		r"   /: \___\  / .  /\  " + "\n" +
		r"   \' / . / /____/..\ " + f"    {__consts__['name']} {__consts__['version']}\n" +
		r"    \/___/  \'  '\  / " + f"    {__consts__['copyright']}\n" +
		r"             \'__'\/  " + "\n"
	)

	print_animated(intro_image, .02)

	running = True
	while running:
		dice = []

		# Get the number of dice that the user would like to roll, from and input and then use `get_first_int()` to convert it.
		num_dice = input('How many dice would you like to roll (default 1)? ')
		num_dice = get_first_int(num_dice, 1)

		# Get the number of faces on each die, at the moment the max is 9, because that is the highest that draw_text() can account for.
		num_faces = input('How many faces do the dice have (default 6, max 9), starting from 1? ')
		num_faces = get_first_int(num_faces, 6)
		print('')

		for i in range(num_dice):
			dice.append(Die(num_faces))

		# Add simple processing / loading animation.
		anim = list('|/-\\') # animation states
		anim_count = 35 # iterations
		anim_dur = 2 # seconds

		for i in range(anim_count):
			print(f'[{anim[i % len(anim)]}]  Loading dice...', end='\r')
			time.sleep(anim_dur / anim_count)

		print(' ' * 20, end='\r')
		print_animated(merge_dice_text(dice), .03)

		running = get_yes_no_bool(input('Run the program again [Yes|no]? '))
		if not running:
			print('Not? Ok, then Goodbye and have a great day further. :)')

