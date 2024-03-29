import pygame

class Square:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.abs_x = x * width
		self.abs_y = y * height
		self.abs_pos = (self.abs_x, self.abs_y)
		self.pos = (x, y)
		self.color = 'light' if (x + y) % 2 == 0 else 'dark'
		self.draw_color = (220, 189, 194) if self.color == 'light' else (53, 53, 53)
		self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 228, 10)
		self.occupying_piece = None
		self.coord = self.get_coord()
		self.highlight = False
		self.promotion = False

		self.rect = pygame.Rect(
			self.abs_x,
			self.abs_y,
			self.width,
			self.height
		)


	def get_coord(self):
		columns = 'abcdefgh'
		return columns[self.x] + str(8 - self.y)


	def draw(self, display):
		if self.highlight:
			pygame.draw.rect(display, self.highlight_color, self.rect)
		else:
			pygame.draw.rect(display, self.draw_color, self.rect)

		if self.promotion:
			centering_rect = self.occupying_piece.img.get_rect()
			centering_rect.center = self.rect.center
			display.blit(self.load_image('knight'), centering_rect.topleft)
			display.blit(self.load_image('bishop'), centering_rect.midtop)
			display.blit(self.load_image('rook'), centering_rect.midleft)
			display.blit(self.load_image('queen'), centering_rect.center)
		elif self.occupying_piece != None:
			centering_rect = self.occupying_piece.img.get_rect()
			centering_rect.center = self.rect.center
			display.blit(self.occupying_piece.img, centering_rect.topleft)
			type_pos = ((centering_rect.midleft[0] + centering_rect.bottomleft[0]) / 2, (centering_rect.midleft[1] + centering_rect.bottomleft[1]) / 2)
			display.blit(self.occupying_piece.type_img, type_pos)


	def load_image(self, piece_type):
		img = pygame.image.load('data/images/pieces/' + self.occupying_piece.color + '_' + piece_type + '.png')
		img = pygame.transform.scale(img, (self.width // 2 - 10, self.height // 2 - 10))
		return img