import pygame

class Piece:
	def __init__(self, pos, color, board):
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		self.color = color
		self.has_moved = False
		img_path = 'data/images/pieces/' + color + '_' + self.piece_type + '.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))
		self.type_img = pygame.image.load('data/images/types/' + self.type + '.png')
		self.type_img = pygame.transform.scale(self.type_img, (board.tile_width - 20, board.tile_height - 50))


	def move(self, board, square, type_chart, force=False):			
		for i in board.squares:
			i.highlight = False

		if square in self.get_valid_moves(board) or force:
			prev_square = board.get_square_from_pos(self.pos)
			self.pos, self.x, self.y = square.pos, square.x, square.y

			prev_square.occupying_piece = None

			# Pokemon chess rules
			if square.occupying_piece is not None:
				opposing_type = square.occupying_piece.type
				if type_chart[opposing_type][self.type] == 1:
					square.occupying_piece = self
				elif type_chart[opposing_type][self.type] == 0.5:
					print('Not very effective...')
					square.occupying_piece = None
				elif type_chart[opposing_type][self.type] == 2:
					print('Super effective!')
					square.occupying_piece = self
					board.turn = 'white' if board.turn == 'black' else 'black'
				else:
					print('It had no effect...')
			else:
				square.occupying_piece = self
			
			board.selected_piece = None
			self.has_moved = True

			# Pawn promotion
			if self.notation == ' ':
				if self.y == 0 or self.y == 7:
					from data.classes.pieces.Queen import Queen
					square.occupying_piece = Queen(
						(self.x, self.y),
						self.color,
						board
					)

			# Move rook if king castles
			if self.notation == 'K':
				if prev_square.x - self.x == 2:
					rook = board.get_piece_from_pos((0, self.y))
					rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
				elif prev_square.x - self.x == -2:
					rook = board.get_piece_from_pos((7, self.y))
					rook.move(board, board.get_square_from_pos((5, self.y)), force=True)

			return True
		else:
			board.selected_piece = None
			return False


	def get_moves(self, board):
		output = []
		for direction in self.get_possible_moves(board):
			for square in direction:
				if square.occupying_piece is not None:
					if square.occupying_piece.color == self.color:
						break
					else:
						output.append(square)
						break
				else:
					output.append(square)
		return output


	def get_valid_moves(self, board):
		output = []
		for square in self.get_moves(board):
			if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
				output.append(square)

		return output


	# True for all pieces except pawn
	def attacking_squares(self, board):
		return self.get_moves(board)