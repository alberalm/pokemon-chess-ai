import pygame
import asyncio

from data.classes.Board import Board

pygame.init()

WINDOW_SIZE = (600, 600)
DETERMINISTIC = False

screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1], DETERMINISTIC)
running = True
mx = 0
my = 0
output = ''
hashtag = False

pygame.display.set_caption("Pokemon Chess")

def draw(display):
	display.fill('white')
	board.draw(display)
	pygame.display.update()


def game_to_str(initial_config, game_moves, result, hashtag):
	output = ''
	for config in initial_config:
		for type in config:
			output += type[:2].title()
		output += ' '
	for i in range(len(game_moves)):
		if i % 2 == 0:
			output += str(i // 2 + 1) + '. '
		output += game_moves[i] + ' '
	if hashtag:
		output = output[:-1] + '#' + ' '
	output += result
	return output


async def main():
	global board, screen, WINDOW_SIZE, DETERMINISTIC, running, mx, my, output, hashtag

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
		await asyncio.sleep(0)
	
	hashtag = False
	font = pygame.font.SysFont('timesnewroman', 40)
	if output == 'Draw by absence of kings':
		text = font.render('Draw by absence of kings', True, (255, 255, 255), (0, 0, 0))
		hashtag = True
		output = '1/2-1/2'
	elif output == 'Draw by 50 move rule':
		text = font.render('Draw by 50 move rule', True, (255, 255, 255), (0, 0, 0))
		output = '1/2-1/2'
	elif output == 'Draw by repetition':
		text = font.render('Draw by repetition', True, (255, 255, 255), (0, 0, 0))
		output = '1/2-1/2'
	elif output == 'White wins!':
		text = font.render('White wins!', True, (255, 255, 255), (0, 0, 0))
		hashtag = True
		output = '1-0'
	elif output == 'Black wins!':
		text = font.render('Black wins!', True, (255, 255, 255), (0, 0, 0))
		hashtag = True
		output = '0-1'
	else:
		text = font.render(output, True, (255, 255, 255), (0, 0, 0))
		output = '1/2-1/2'
	textRect = text.get_rect()
	
	# set the center of the rectangular object.
	textRect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)
	screen.blit(text, textRect)

	print(game_to_str(board.initial_config, board.game_moves, output, hashtag))

	pygame.quit()
	quit()

asyncio.run(main())