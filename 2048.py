from numpy import array, arange, full, zeros, isin, append
from numpy.random import choice
import random
from itertools import product
from dataclasses import dataclass


def useless_f(x):
	return x * (x != 0) + (x == 0)

@dataclass
class Board():
	size: int
	final_score: int
	score: int = 0

	def __post_init__(self):
		self.board: array = zeros((self.size, self.size))
		self.blocked: array = full((self.size, self.size), False)

	def add_random_tile(self):
		candidates = []
		for x, y in product(arange(self.size), repeat=2):
			if self.board[y][x] == 0:
				candidates.append((y, x))

		decision = random.choice(candidates)
		num = choice(array([2, 4]), p=[0.9, 0.1])
		self.board[decision[0]][decision[1]] = num
		return self.board

	def available_actions(self):
		actions = array([])

		def add_action_x(direction, index, actions):
			try:
				if self.board[y][index] in [self.board[y][x], 0]:
					if not isin(direction, actions):
						actions = append(actions, direction)
				return actions

			except IndexError:
				return actions

		def add_action_y(direction, index, actions):
			try:
				if self.board[index][x] in[self.board[y][x], 0]:
					if not isin(direction, actions):
						actions = append(actions, direction)
				return actions

			except IndexError:
				return actions

		for x, y in product(arange(self.size), repeat=2):
			if self.board[y][x] != 0:
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

		for x, y in product(arange(self.size)[::-useless_f(k[0])],
						    arange(self.size)[::-useless_f(k[1])]):

			if self.board[y][x] != 0:
				sign = self.board[y][x]
				self.board[y][x] = 0

				if k[0] != 0: 
					x_range = arange(0+(x+1)*(k[0]>0), x+(self.size-x)*(k[0]>0))[::k[0]]

					if x_range.size == 0:
						self.board[y][x] = sign
					

					for x1 in x_range:
						if self.board[y][x1] == sign and not self.blocked[y][x1]:
							self.board[y][x1] = sign * 2
							self.score += sign * 2
							self.blocked[y][x1] = True
							break
						elif self.board[y][x1] != 0:
							self.board[y][x1-k[0]] = sign
							break
					
						elif x1 == 0 or x1 == self.size - 1:
							self.board[y][x1] = sign
							break
				else:
					y_range = arange(0+(y+1)*(k[1]>0), y+(self.size-y)*(k[1]>0))[::k[1]]

					if y_range.size == 0:
						self.board[y][x] = sign

					for y1 in y_range:
						if self.board[y1][x] == sign and not self.blocked[y1][x]:
							self.board[y1][x] = sign * 2
							self.score += sign * 2
							self.blocked[y1][x] = True
							break
						elif self.board[y1][x] != 0:
							self.board[y1-k[1]][x] = sign
							break
						elif y1 == 0 or y1 == self.size - 1:
							self.board[y1][x] = sign
							break

		self.blocked[self.blocked==True] = False


def run():
	board = Board(4, 2048)
	board.add_random_tile()

	while True:
		print(board.board)

		options = board.available_actions()
		if board.score == board.final_score:
			print('You won!')
			break

		elif options.size == 0:
			print('Game Over! No moves available!')
			break

		print(f'Your score: {board.score}')
		print(f'Available moves: {options}')
		
		while True:
			next_move = input('It your next move: ')
			if next_move in options:
				break
		
		board.move(next_move)
		board.add_random_tile()


run()