from email.charset import add_charset
import numpy as np
from random import choice
from itertools import product


def useless_f(x):
	if x == 0:
		return 1

	return x


class Board():
	def __init__(self, size, final_score) -> None:
		self.size = size
		self.final_score = final_score

		self.board = np.zeros((size, size), dtype=np.int8)
		self.blocked = np.full((size, size), False)
		self.score = 0

	def __repr__(self):
		result = ''

		for x in np.arange(self.size):
			new_line = ''
			for y in np.arange(self.size):
				new_line = ' | '.join([new_line, str(self.board[y][x])])
			new_line += '\n' + '---' * (self.size + 2)
			result += new_line + '\n'

		return result


	def add_random_tile(self):
		candidates = []
		for x, y in product(np.arange(self.size), repeat=2):
			if self.board[y][x] == 0:
				candidates.append((y, x))

		decision = choice(candidates)
		num = np.random.choice(np.array([2, 4]), p=[0.9, 0.1])
		self.board[decision[0]][decision[1]] = num
		return self.board

	def available_actions(self):
		actions = np.array([])

		def add_action_x(direction, index, actions):
			try:
				if self.board[index][y] == self.board[x][y] or self.board[index][y] == 0:
					if not np.isin(direction, actions):
						actions = np.append(actions, direction)
				return actions

			except IndexError:
				return actions

		def add_action_y(direction, index, actions):
			try:
				if self.board[x][index] == self.board[x][y] or self.board[x][index] == 0:
					if not np.isin(direction, actions):
						actions = np.append(actions, direction)
				return actions

			except IndexError:
				return actions

		for x, y in product(np.arange(self.size), repeat=2):
			if self.board[x][y] != 0:
				actions = add_action_x(direction='LEFT',  index=x-1, actions=actions)
				actions = add_action_x(direction='RIGHT', index=x+1, actions=actions)
				actions = add_action_y(direction='UP',    index=y-1, actions=actions)
				actions = add_action_y(direction='DOWN',  index=y+1, actions=actions)

			if actions.size == 4:
				return actions

		return actions

	def move(self, direction):
		convert_dict = {
			'LEFT':  (-1,  0),
			'RIGHT': ( 1,  0),
			'UP':    ( 0, -1),
			'DOWN':  ( 0,  1)
		}

		k = convert_dict[direction]

		for x, y in product(np.arange(self.size)[::-useless_f(k[0])],
						    np.arange(self.size)[::-useless_f(k[1])]):

			if self.board[x][y] != 0:
				sign = self.board[x][y]
				self.board[x][y] = 0

				if k[0] != 0: 
					if k[0] == -1:
						x_range = np.arange(0, x)[::-1]
					else:
						x_range = np.arange(x+1, self.size)

					if x_range.size == 0:
						self.board[x][y] = sign
					

					for x1 in x_range:
						if self.board[x1][y] == sign and not self.blocked[x1][y]:
							self.board[x1][y] = sign * 2
							self.score += sign * 2
							self.blocked[x1][y] = True
							break
						elif self.board[x1][y] != 0:
							self.board[x1-k[0]][y] = sign
							break
					
						elif x1 == 0 or x1 == self.size - 1:
							self.board[x1][y] = sign
							break
				else:
					if k[1] == -1:
						y_range = np.arange(0, y)[::-1]
					else:
						y_range = np.arange(y+1, self.size)

					if y_range.size == 0:
						self.board[x][y] = sign

					for y1 in y_range:
						if self.board[x][y1] == sign and not self.blocked[x][y1]:
							self.board[x][y1] = sign * 2
							self.score += sign * 2
							self.blocked[x][y1] = True
							break
						elif self.board[x][y1] != 0:
							self.board[x][y1-k[1]] = sign
							break
						elif y1 == 0 or y1 == self.size - 1:
							self.board[x][y1] = sign
							break
		self.blocked = np.full((self.size, self.size), False)


def run():
	board = Board(4, 2048)
	board.add_random_tile()
	score = 0

	while True:
		print(board)

		options = board.available_actions()
		if options.size == 0:
			print('Game Over! No moves available!')
			break

		print(f'Your score: {board.score}')
		print(f'Available moves: {options}')
		
		while True:
			next_move = input('Input your next move: ')
			if next_move in options:
				break
		
		board.move(next_move)
		board.add_random_tile()


run()


			