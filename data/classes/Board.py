import pygame

from data.classes.Square import Square
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn
from data.classes.csv_reader import *

# Game state checker
class Board:
	def __init__(self, width, height, deterministic):
		self.width = width
		self.height = height
		self.tile_width = width // 8
		self.tile_height = height // 8
		self.selected_piece = None
		self.turn = 'white'
		self.chain_move = False
		self.en_passant = None
		self.moves_until_draw = 100
		self.game_moves = []
		self.current_move = ""
		self.positions = {}
		self.white_castle = 2
		self.black_castle = 2
		self.draw_by_repetition = False
		self.promotion = False
		self.deterministic = deterministic

		self.white_config = read_config('white_config.csv')
		self.black_config = read_config('black_config.csv')

		self.initial_config = self.white_config + self.black_config

		self.type_chart = read_type_chart('type_chart.csv')

		self.config = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['-','-','-','-','-','-','-','-'],
			['-','-','-','-','-','-','-','-'],
			['-','-','-','-','-','-','-','-'],
			['-','-','-','-','-','-','-','-'],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
		]

		for i in range(8):
			self.config[0][i] += self.black_config[1][i]
			self.config[1][i] += self.black_config[0][i]
			self.config[6][i] += self.white_config[0][i]
			self.config[7][i] += self.white_config[1][i]

		self.update_positions()

		self.squares = self.generate_squares()

		self.setup_board()


	def generate_squares(self):
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(x,  y, self.tile_width, self.tile_height)
				)
		return output


	def get_square_from_pos(self, pos):
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square


	def get_piece_from_pos(self, pos):
		return self.get_square_from_pos(pos).occupying_piece
	

	def add_disambiguation(self, piece, square, prev_square):
		if piece.notation != ' ':
			pieces = [sq for sq in self.squares if sq.occupying_piece != None and \
				sq.occupying_piece.color == piece.color and \
					sq.occupying_piece.notation == piece.notation and \
						square in sq.occupying_piece.get_valid_moves(self) and \
							sq.occupying_piece.type != piece.type]
			if len(pieces) > 0:
				row_match = False
				col_match = False
				for p in pieces:
					if p.x == prev_square.x:
						row_match = True
					if p.y == prev_square.y:
						col_match = True
				if not row_match:
					self.current_move += chr(prev_square.x + 97)
				elif not col_match:
					self.current_move += str(8 - prev_square.y)
				else:
					self.current_move += chr(prev_square.x + 97) + str(8 - prev_square.y)


	def setup_board(self):
		# iterating 2d list
		for y, row in enumerate(self.config):
			for x, piece in enumerate(row):
				if piece != '-':
					square = self.get_square_from_pos((x, y))

					# looking inside contents, what piece does it have
					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y), 'white' if piece[0] == 'w' else 'black', self, piece[2:]
						)

					elif piece[1] == 'N':
						square.occupying_piece = Knight(
							(x, y), 'white' if piece[0] == 'w' else 'black', self, piece[2:]
						)

					elif piece[1] == 'B':
						square.occupying_piece = Bishop(
							(x, y), 'white' if piece[0] == 'w' else 'black', self, piece[2:]
						)

					elif piece[1] == 'Q':
						square.occupying_piece = Queen(
							(x, y), 'white' if piece[0] == 'w' else 'black', self, piece[2:]
						)

					elif piece[1] == 'K':
						square.occupying_piece = King(
							(x, y), 'white' if piece[0] == 'w' else 'black', self, piece[2:]
						)

					elif piece[1] == 'P':
						square.occupying_piece = Pawn(
							(x, y), 'white' if piece[0] == 'w' else 'black', self, piece[2:]
						)


	def handle_click(self, mx, my):
		x = mx // self.tile_width
		y = my // self.tile_height
		clicked_square = self.get_square_from_pos((x, y))

		if self.promotion:
			if clicked_square.promotion:
				self.promotion = False
				clicked_square.promotion = False
				if mx < clicked_square.abs_x + self.tile_width // 2 and \
					  my < clicked_square.abs_y + self.tile_height // 2:
					piece = Knight
				elif mx >= clicked_square.abs_x + self.tile_width // 2 and \
					  my < clicked_square.abs_y + self.tile_height // 2:
					piece = Bishop
				elif mx < clicked_square.abs_x + self.tile_width // 2 and \
					  my >= clicked_square.abs_y + self.tile_height // 2:
					piece = Rook
				elif mx >= clicked_square.abs_x + self.tile_width // 2 and \
					  my >= clicked_square.abs_y + self.tile_height // 2:
					piece = Queen
				clicked_square.occupying_piece = piece(
						(clicked_square.x, clicked_square.y),
						clicked_square.occupying_piece.color,
						self,
						clicked_square.occupying_piece.type
						)
				modifier = self.current_move[-1] if self.chain_move else ''
				self.current_move = self.current_move[:-1] + '=' + clicked_square.occupying_piece.notation
				if self.chain_move:
						self.selected_piece = clicked_square.occupying_piece
						self.current_move += modifier
				if not self.chain_move or self.game_finished() != '':
					self.end_turn()

		elif self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece

		elif self.selected_piece.move(self, clicked_square, self.type_chart):
			if not self.promotion:
				if not self.chain_move or self.game_finished() != '':
					self.end_turn()

		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == self.turn:
				if not self.chain_move:
					self.selected_piece = clicked_square.occupying_piece
				elif self.selected_piece == clicked_square.occupying_piece:
					self.selected_piece = None
					self.end_turn()

	
	def end_turn(self):
		self.turn = 'white' if self.turn == 'black' else 'black'
		self.moves_until_draw -= 1
		self.game_moves.append(self.current_move)
		self.current_move = ""
		self.update_config()
		self.update_positions()


	def update_config(self):
		self.config = [[self.get_piece_from_pos((x, y)).to_string() if \
				  self.get_piece_from_pos((x, y)) != None else '-' for x in range(8)] \
					for y in range(8)]
		
	
	def update_positions(self):
		c = ''.join([''.join([j[:4] for j in i]) for i in self.config])
		c += str(self.white_castle) + str(self.black_castle) + self.turn[0]
		if c not in self.positions:
			self.positions[c] = 1
		else:
			self.positions[c] += 1
			if self.positions[c] == 3:
				self.draw_by_repetition = True


	def game_finished(self):
		output = ''
		w_king = None
		b_king = None
		
		if not self.promotion:
			if self.moves_until_draw == 0:
				output = 'Draw by 50 move rule'
			elif self.draw_by_repetition:
				output = 'Draw by repetition'
			else:
				for piece in [i.occupying_piece for i in self.squares]:
					if piece != None:
						if piece.notation == 'K':
							if piece.color == 'white':
								w_king = piece
							else:
								b_king = piece
					if w_king != None and b_king != None:
						break
				if w_king == None:
					if b_king == None:
						output = 'Draw by absence of kings'
					else:
						output = 'Black wins!'
				elif b_king == None:
					output = 'White wins!'

		return output


	def draw(self, display):
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)