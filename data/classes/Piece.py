import pygame
import random

class Piece:
	def __init__(self, pos, color, board):
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		self.color = color
		self.has_moved = False
		img_path = 'data/images/pieces/' + color + '_' + self.piece_type.lower() + '.png'
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
			rand = random.randint(1, 160)

			# This may not be accurate
			miss = rand <= 16 # 1/10 chance to miss
			critical_hit = rand >= 150 # 1/16 chance to critical hit

			if square.occupying_piece is not None:
				capture = True
				opposing_type = square.occupying_piece.type

			# En passant
			if self.notation == ' ' and square == board.en_passant and prev_square.x != square.x:
				if not miss:
					capture = True
					captured_square = board.get_square_from_pos((square.x, prev_square.y))
					opposing_type = captured_square.occupying_piece.type
					if type_chart[self.type][opposing_type] != 0:
						captured_square.occupying_piece = None
			
			if board.current_move == '' and (self.notation != 'K' or abs(prev_square.x - self.x) != 2):
				board.current_move = self.notation if self.notation != ' ' else \
					(prev_square.coord[0] if capture else '')
				board.add_disambiguation(self, square, prev_square)
			
			if capture:
				board.current_move += 'x'
				# Pokemon chess rules
				output = ''
				modifier = ''
				previous_piece = square.occupying_piece
				if type_chart[self.type][opposing_type] == '1':
					square.occupying_piece = self
					board.current_move += square.coord
				elif type_chart[self.type][opposing_type] == '0.5':
					output = 'Not very effective...'
					square.occupying_piece = None
					board.current_move += square.coord
					modifier = '-'
				elif type_chart[self.type][opposing_type] == '2':
					output = 'Super effective!'
					square.occupying_piece = self
					board.chain_move = True
					board.current_move += square.coord
					modifier = '+'
				else:
					output = 'It had no effect...'
					self.pos, self.x, self.y = prev_square.pos, prev_square.x, prev_square.y
					prev_square.occupying_piece = self
				if type_chart[self.type][opposing_type] != '0' and miss:
					output = self.piece_type + '\'s attack missed!'
					board.chain_move = False
					prev_square.occupying_piece = self
					self.pos, self.x, self.y = prev_square.pos, prev_square.x, prev_square.y
					square.occupying_piece = previous_piece
					modifier = '/'
				elif critical_hit and (type_chart[self.type][opposing_type] == '1' or
						   type_chart[self.type][opposing_type] == '0.5'):
					output = 'Critical hit!'
					board.chain_move = True
					modifier = '*'
					square.occupying_piece = self
				if output != '':
					print(output)
					board.current_move += modifier
				if type_chart[self.type][opposing_type] != '0' and not miss:
					board.moves_until_draw = 101
			else:
				square.occupying_piece = self
				board.current_move += square.coord
			
			if board.chain_move == False:
				board.selected_piece = None
			
			if prev_square.occupying_piece == None: # No misses or no x0 effectiveness
				if self.notation == 'R' and not self.has_moved:
					if self.color == 'white':
						board.white_castle -= 1
					else:
						board.black_castle -= 1
				self.has_moved = True

			if self.notation == ' ' and prev_square.occupying_piece == None:
				board.moves_until_draw = 101
				# En passant setup
				if self.color == 'white' and self.y == 4 and prev_square.y == 6:
					board.en_passant = board.get_square_from_pos((self.x, 5))
				elif self.color == 'black' and self.y == 3 and prev_square.y == 1:
					board.en_passant = board.get_square_from_pos((self.x, 2))
				# Pawn promotion
				elif (self.y == 0 or self.y == 7) and square.occupying_piece == self:
					board.en_passant = None
					board.promotion = True
					square.promotion = True
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
				if prev_square.occupying_piece == None:
					if self.color == 'white':
						board.white_castle = 0
					else:
						board.black_castle = 0

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
	
	
	def to_string(self):
		return self.color[0] + (self.notation if self.notation != ' ' else 'P') + self.type