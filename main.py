import pygame

from data.classes.Board import Board

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1])

def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()


def print_game(game_moves, result):
	output = ''
	for i in range(len(game_moves)):
		if i % 2 == 0:
			output += str(i // 2 + 1) + '. '
		output += game_moves[i] + ' '
	output += result
	return output


if __name__ == '__main__':
	running = True
	while running:
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():
			# Quit the game if the user presses the close button
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: 
       			# If the mouse is clicked
				if event.button == 1:
					board.handle_click(mx, my)
		output = board.game_finished()
		if output != '':
			print(output)
			running = False
		# Draw the board
		draw(screen)
	if output == '' or output == 'Draw by 50 move rule' or \
		output == 'Draw by 3-fold repetition' or output == 'Draw by absence of kings':
		output = '1/2-1/2'
	elif output == 'White wins!':
		output = '1-0'
	elif output == 'Black wins!':
		output = '0-1'
	print(print_game(board.game_moves, output))