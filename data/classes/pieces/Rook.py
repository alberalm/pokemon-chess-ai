import pygame

from data.classes.Piece import Piece

class Rook(Piece):
	def __init__(self, pos, color, board, type):
		self.piece_type = 'rook'
		self.type = type
		super().__init__(pos, color, board)

		self.notation = 'R'


	def get_possible_moves(self, board):
		output = []

		moves_north = []
		for y in range(self.y)[::-1]:
			moves_north.append(board.get_square_from_pos(
				(self.x, y)
			))
		output.append(moves_north)

		moves_east = []
		for x in range(self.x + 1, 8):
			moves_east.append(board.get_square_from_pos(
				(x, self.y)
			))
		output.append(moves_east)

		moves_south = []
		for y in range(self.y + 1, 8):
			moves_south.append(board.get_square_from_pos(
				(self.x, y)
			))
		output.append(moves_south)

		moves_west = []
		for x in range(self.x)[::-1]:
			moves_west.append(board.get_square_from_pos(
				(x, self.y)
			))
		output.append(moves_west)

		return output
