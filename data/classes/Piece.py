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


	def move(self, board, square, type_chart):
		for i in board.squares:
			i.highlight = False

		if square in self.get_valid_moves(board):
			board.chain_move = False
			prev_square = board.get_square_from_pos(self.pos)
			self.pos, self.x, self.y = square.pos, square.x, square.y

			prev_square.occupying_piece = None

			capture = False

			if square.occupying_piece is not None:
				capture = True
				opposing_type = square.occupying_piece.type

			# En passant
			if self.notation == ' ' and square == board.en_passant and prev_square.x != square.x:
				capture = True
				captured_square = board.get_square_from_pos((square.x, prev_square.y))
				opposing_type = captured_square.occupying_piece.type
				if type_chart[opposing_type][self.type] != 0:
					captured_square.occupying_piece = None
			
			if board.current_move == '' and (self.notation == 'K' or abs(prev_square.x - self.x) != 2):
				board.current_move = self.notation if self.notation != ' ' else \
					(prev_square.coord[0] if capture else '')
			
			if capture:
				board.current_move += 'x'
				# Pokemon chess rules
				board.moves_until_draw = 101
				if type_chart[opposing_type][self.type] == 1:
					square.occupying_piece = self
					board.current_move += square.coord
				elif type_chart[opposing_type][self.type] == 0.5:
					print('Not very effective...')
					square.occupying_piece = None
					board.current_move += square.coord + '-'
				elif type_chart[opposing_type][self.type] == 2:
					print('Super effective!')
					square.occupying_piece = self
					board.chain_move = True
					board.current_move += square.coord + ('+' if self.notation != ' ' or
										   (self.y != 0 and self.y != 7) else '')
				else:
					print('It had no effect...')
					self.pos, self.x, self.y = prev_square.pos, prev_square.x, prev_square.y
					prev_square.occupying_piece = self
			else:
				square.occupying_piece = self
				board.current_move += square.coord
			
			if board.chain_move == False:
				board.selected_piece = None
			self.has_moved = True

			# Pawn promotion
			if self.notation == ' ':
				board.moves_until_draw = 101
				if self.color == 'white' and self.y == 4 and prev_square.y == 6:
					board.en_passant = board.get_square_from_pos((self.x, 5))
				elif self.color == 'black' and self.y == 3 and prev_square.y == 1:
					board.en_passant = board.get_square_from_pos((self.x, 2))
				elif self.y == 0 or self.y == 7:
					from data.classes.pieces.Queen import Queen
					board.en_passant = None
					square.occupying_piece = Queen(
						(self.x, self.y),
						self.color,
						board,
						self.type
					)
					board.current_move += '=' + square.occupying_piece.notation
					if board.chain_move:
						board.selected_piece = square.occupying_piece
						board.current_move += '+'
						# CHANGE THIS WHEN CRITICAL HITS ARE IMPLEMENTED
				elif not board.chain_move:
					board.en_passant = None
			else:
				board.en_passant = None

			# Move rook if king castles
			if self.notation == 'K':
				if prev_square.x - self.x == 2:
					rook = board.get_piece_from_pos((0, self.y))
					board.get_square_from_pos(rook.pos).occupying_piece = None
					rook.pos, rook.x, rook.y = (3, self.y), 3, self.y
					board.get_square_from_pos((3, self.y)).occupying_piece = rook
					board.current_move = 'O-O-O'
				elif prev_square.x - self.x == -2:
					rook = board.get_piece_from_pos((7, self.y))
					board.get_square_from_pos(rook.pos).occupying_piece = None
					rook.pos, rook.x, rook.y = (5, self.y), 5, self.y
					board.get_square_from_pos((5, self.y)).occupying_piece = rook
					board.current_move = 'O-O'

			return True
		elif not board.chain_move:
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
		return self.get_moves(board)


	# True for all pieces except pawn
	def attacking_squares(self, board):
		return self.get_moves(board)