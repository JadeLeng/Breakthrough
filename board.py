from copy import deepcopy
import numpy as np
import define
import math

class board:
	def __init__(self, type):
		self.length = 8
		self.width = 8
		self.boardtype = define.SQUARE
		if type == define.SQUARE:
			self.state = np.array([
				[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0],
				[0,0,0,0,0,0,0,0],
				[2,2,2,2,2,2,2,2],
				[2,2,2,2,2,2,2,2]
				])
			self.boardtype = define.SQUARE
			self.length = 8
			self.width = 8
			self.bothchess = 16
		else:
			self.state = np.array([
				[1,1,1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1,1,1],
				[0,0,0,0,0,0,0,0,0,0],
				[2,2,2,2,2,2,2,2,2,2],
				[2,2,2,2,2,2,2,2,2,2]
				])
			self.boardtype = define.RECTANGLE
			self.length = 5
			self.width = 10
			self.bothchess = 20
		


		self.capture1 = 0 # Number of captured player_1
		self.capture2 = 0 # Number of captured player_2
		self.changestep = []
		
	def move_pseudo(self, curpos, nextpos):
		# calculate the captured pieces
		if self.state[nextpos[0]][nextpos[1]] != self.state[curpos[0]][curpos[1]]:
			if self.state[curpos[0]][curpos[1]] == define.PLAYER_1:
				self.capture2 += 1
			else:
				self.capture1 += 1
		# cover the next pos
		self.state[nextpos[0]][nextpos[1]] = self.state[curpos[0]][curpos[1]]
		self.state[curpos[0]][curpos[1]] = 0
		self.changestep.append((curpos, nextpos))


	def move(self, curpos, nextpos):
		# define capture
		if self.state[nextpos[0]][nextpos[1]] == define.PLAYER_2 and self.state[curpos[0]][curpos[1]] == define.PLAYER_1:
			self.capture2 += 1
		elif self.state[nextpos[0]][nextpos[1]] == define.PLAYER_1 and self.state[curpos[0]][curpos[1]] == define.PLAYER_2:
			self.capture1 += 1
		# cover the next pos
		self.state[nextpos[0]][nextpos[1]] = self.state[curpos[0]][curpos[1]]
		self.state[curpos[0]][curpos[1]] = 0
		self.changestep.append((curpos, nextpos))

	def boardcopy(self):
		b = board(self.boardtype)
		for y in range(b.length):
			for x in range(b.width):
				b.state[y][x] = self.state[y][x]


		# b.state = deepcopy(self.state)
		b.capture1 = self.capture1
		b.capture2 = self.capture2
		b.changestep = []
		for step in self.changestep:
			b.changestep.append(step)
		# b.changestep = self.changestep
		# print (id(self),id(b))
		return b


	def printnext(self, player, curpos):
		#nextboards = []
		x = curpos[1]
		y = curpos[0]
		# find the next step for player 1
		if player is define.PLAYER_1:
			if self.state[y][x] == define.PLAYER_1 and y + 1 < self.length:
				if x - 1 >= 0 and self.state[y+1][x-1] != define.PLAYER_1:
					# could move
					print ("could move", curpos, (y+1,x-1))
					
				if x + 1 < self.width and self.state[y+1][x+1] != define.PLAYER_1:
					print ("could move", curpos, (y+1,x+1))
					
				# not caputure: (y+1, x) is 0
				if self.state[y+1][x] == 0:
					print ("could move", curpos, (y+1,x))
					
		
		elif player is define.PLAYER_2:
			if self.state[y][x] == define.PLAYER_2 and y - 1 >= 0:
				if x - 1 >= 0 and self.state[y-1][x-1] != define.PLAYER_2:
					# could move
					print ("could move", curpos, (y-1,x-1))
						
				if x + 1 < self.width and self.state[y-1][x+1] != define.PLAYER_2:
					print ("could move", curpos, (y-1,x+1))
						
					# not caputure: (y+1, x) is 0
				if self.state[y-1][x] == 0:
					print ("could move", curpos, (y-1,x))
	'''
	def next_pseudo(self, player):
		nextboards = []
		count = 0 # this is to cut loop for unnecessary search if we get all the pieces
		if player == define.PLAYER_1:
			for y in range(self.length):
				for x in range(self.width):
					if self.state[y][x] == define.PLAYER_1 and y + 1 < self.length:
						# cut down the unnecessary search part
						if count == self.calculate_alive(player):
							return nextboards
						# list all three possible position for player 1: (y+1, x-1), (y+1, x), (y+1, x+1)
						if x - 1 >= 0 and self.state[y+1][x-1] != define.PLAYER_1:
							cur = board.copy() # generate a new board
							cur.move((y,x), (y+1, x-1))
							nextboards.append(cur)
							count += 1
						if x + 1 >= 0 and self.state[y+1][x+1] != define.PLAYER_1:
							# the same with above
						if self.state[y+1][x] == 0:
							# the same with above
		else:
			# for player_2, vice versa

		return nextboards
	'''



	def next(self, player):
		nextboards = []
		count = 0
		# find the next step for player 1
		if player is define.PLAYER_1:
			for y in range(self.length):
				#y = self.length - y - 1
				for x in range(self.width):
					# find the postion for player_1
					'''
					if (self.state[y][x] == define.PLAYER_1):
						print (y,x, self.state[y][x])
					else:
						print (y,x)
					'''
					if self.state[y][x] == define.PLAYER_1 and y + 1 < self.length:
						# find the next move, could be in 3 directions, x-1, x, x+1
						# print (self.state[y][x])
						
						if count == self.calculate_alive(player):
							return nextboards
						if x - 1 >= 0 and self.state[y+1][x-1] != define.PLAYER_1:
							# could move
							cur = self.boardcopy()
							
							cur.move((y,x),(y+1,x-1))
							nextboards.append(cur)
						if x + 1 < self.width and self.state[y+1][x+1] != define.PLAYER_1:
							cur = self.boardcopy()
							
							cur.move((y,x),(y+1,x+1))
							nextboards.append(cur)
						# not caputure: (y+1, x) is 0
						if self.state[y+1][x] == 0:
							cur = self.boardcopy()
							
							cur.move((y,x), (y+1,x))
							nextboards.append(cur)
						count += 1
		
		elif player is define.PLAYER_2:
			for y in range(self.length):
				y = self.length - y - 1
				for x in range(self.width):
					# find the postion for player_2
					if self.state[y][x] == define.PLAYER_2 and y - 1 >= 0:
						if count == self.calculate_alive(player):
							return nextboards

						# find the next move, could be in 3 directions, x-1, x, x+1

						if x - 1 >= 0 and self.state[y-1][x-1] != define.PLAYER_2:
							# could move
							cur = self.boardcopy()
							cur.move((y,x),(y-1,x-1))
							nextboards.append(cur)
						if x + 1 < self.width and self.state[y-1][x+1] != define.PLAYER_2:
							cur = self.boardcopy()
							cur.move((y,x),(y-1,x+1))
							nextboards.append(cur)
						# not caputure: (y+1, x) is 0
						if self.state[y-1][x] == 0:
							cur = self.boardcopy()
							cur.move((y,x), (y-1,x))
							nextboards.append(cur)
						count += 1

		return nextboards

	# return the number of alive ones
	def calculate_alive(self, whoami):
		if whoami is define.PLAYER_1:
			return self.bothchess-self.capture1
		else:
			return self.bothchess-self.capture2


	def calculate_capture(self, whoami):
		if whoami is define.PLAYER_1:
			return self.capture2
		else:
			return self.capture1

	'''
	def mydist_pseudo(self, whoami, expo):
		dist = 0
		count = 0

		for y in range(self.length):
			if whoami == self.PLAYER_1:
				# make the calculation easier
				y = self.length - y - 1
			for x in range(self.width):
				if self.state[y][x] == whoami:
					if count == self.calculate_alive(whoami):
						# also for better performance
						return dist
					if whoami is define.PLAYER_1:
						dist += math.pow(expo, y)
						if y == self.length - 1:
							return define.WINVALUE
						if y == self.length - 2:
							return define.NEARWINVALUE
					else:
						# the same with player 2 except y should be length-y+1
					count += 1
	'''


	def mydist(self, whoami, expo):
		dist = 0
		count = 0
		for y in range(self.length):
			for x in range(self.width):
				if self.state[y][x] == whoami:
					if count == self.calculate_alive(whoami):
						return dist
					if whoami is define.PLAYER_1:
						dist+= math.pow(expo,y)
						if y == self.length - 1:
							return 2048
						if  y == self.length-2:
							return 1024
					else:
						dist+= math.pow(expo,self.length-y+1)
						if y== 0:
							return 2048
						if y == 1:
							return 1024
					count += 1
		return dist

	def mydist_3(self, whoami, expo):
		dist = 0
		count = 0
		count_3 = 0
		for y in range(self.length):
			for x in range(self.width):
				if self.state[y][x] == whoami:
					if count == self.calculate_alive(whoami):
						return dist
					if whoami is define.PLAYER_1:
						dist+= math.pow(expo,y)
						if y == self.length - 1 or y == self.length-2:
							count_3 += 1
							dist += 40
							if count_3 == 3:
								return 2048

					else:
						dist+= math.pow(expo,self.length-y+1)
						if y == 1 or y== 0:
							count_3 += 1
							dist += 40
							if count_3 == 3:
								return 2048
					count += 1
		return dist

	def homestate(self, whoami):
		count = 0
		if whoami is define.PLAYER_1:
			for x in range(self.width):
				if self.state[0][x] == define.PLAYER_1:
					count += 1
		else:
			for x in range(self.width):
				if self.state[self.length-1][x] == define.PLAYER_2:
					count += 1
		return count
	


	def clearstep(self):
		self.changestep = []
