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


def game_to_str(game_moves, result, hashtag):
	output = ''
	for i in range(len(game_moves)):
		if i % 2 == 0:
			output += str(i // 2 + 1) + '. '
		output += game_moves[i] + ' '
	if hashtag:
		output = output[:-1] + '#' + ' '
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
	hashtag = False
	if output[:4] == 'Draw':
		if output == 'Draw by absence of kings':
			hashtag = True
		output = '1/2-1/2'
	elif output == 'White wins!':
		hashtag = True
		output = '1-0'
	elif output == 'Black wins!':
		hashtag = True
		output = '0-1'
	print(game_to_str(board.game_moves, output, hashtag))