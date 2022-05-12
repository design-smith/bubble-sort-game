#importing the required modules 
from curses import window
from tkinter import Label
import pygame
import random
import math

pygame.init()

class DrawInformation:
#colours
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	PINK = 255, 0, 128
	ORANGE = 255, 128, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('comicsans', 30)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Bubble Sort Visualization with TechVidvan")#setting the caption
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)#minimum of the list
		self.max_val = max(lst)#maximum of the list

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))#rounding off
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2



def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)#filling the background
	draw_list(draw_info)
	show(draw_info)
	pygame.display.update()#updating the screen

def show(draw_info):
	lst = draw_info.lst
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)
	block =  draw_info.FONT.render(str(lst), True, (0,0,0))
    #Display the array
	draw_info.window.blit(block, (0,20))


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)#drawing rectangle

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()

def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.PINK, j + 1: draw_info.ORANGE}, True)
				yield True
		#making a new array to display
		array1 = [str(i) for i in lst]
		array1=",".join(array1)

    	
	return lst

def main():
	run = True
	clock = pygame.time.Clock()
	lst=[]#empty list
	n = int(input("Enter number of elements : "))
# iterating till the range
	for i in range(0, n):
		ele=int(input())
		lst.append(ele)
	draw_info = DrawInformation(800, 600, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(5)#how many frames per second

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"


	pygame.quit()

#calling main method
if __name__ == "__main__":
	main()