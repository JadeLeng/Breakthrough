import numpy as np
import math
import random
from board import board
import define

class player:
	def __init__(self, rule, strategy, attack, depth, whoami, type):
		self.strategy = strategy
		self.attack = attack
		self.depth = depth
		self.time = 0
		self.step = 0
		self.whoami = whoami
		self.node = 0
		self.type = type
		self.rule = rule

	def move(self, board):
		if self.strategy is define.MINMAX:
			# print ("MINMAX")
			# max is always myself while my opponent want it to be min
			board.clearstep()
			ret = self.minmax(board, 0, define.MAX, self.whoami)
			#print (ret[1].state)
			step = ret[1].changestep[0]
			#print (step)
			return step
		else:
			# print("ALPHABETA")
			board.clearstep()
			ret = self.alphabeta(board, 0, define.MAX)
			#print (ret[1].state)
			step = ret[1].changestep[0]
			return step
			

	def minmax(self, board, depth, minormax, whoami):
		# self.node += 1
		# a recursion for generating queue-based node expansion
		if self.depth is depth:
			# return board and heursic
			if self.attack is define.DEFENSIVE:
				h = self.heursic_defensive(board, minormax, whoami, self.type)
			else:
				h = self.heursic_offensive(board, minormax, whoami, self.type)
			return (h, board)

		# recursion
		queue = []
		boards = board.next(whoami)
		# print (board.state)
		if (len(boards) == 0):
			#print (board.state)
			pass

		for b in boards:
			queue.append(self.minmax(b, depth+1, 1-minormax, 3-whoami))
		queue = sorted(queue)
		
		if (len(queue) == 0):
			# return board and heursic
			if self.attack is define.DEFENSIVE:
				h = self.heursic_defensive(board, minormax, whoami, self.type)
			else:
				h = self.heursic_offensive(board, minormax, whoami, self.type)
			return (h, board)

		# print (queue)
		if minormax is define.MAX:
			return queue[-1]
		else:
			return queue[0]

	def alphabeta(self, board, depth, minormax):
		if minormax is define.MAX:
			return self.ab_max(board, depth, minormax, -np.inf, np.inf, self.whoami)
		else:
			return self.ab_min(board, depth, minormax, -np.inf, np.inf, self.whoami)

	def heursic_defensive(self, board, minormax, whoami, type):
		# self.node+=1
		if type is 1:
			if minormax is define.MAX:
				get_alive = board.calculate_alive(whoami)
				return 2*get_alive + random.random()			
			else:
				# Acutally I don't know what's my opponent's strategy
				# in my enemy(whoami)'s min level, he still want to know my heuristic
				get_alive = board.calculate_alive(3-whoami)
				return 2*get_alive + random.random()
		elif type is 2:
			# first of all, the more I have*weight
			# second of all, the less my opponent would touch my baseline
			# make my distance to lose to be large as possible

			if self.rule == define.RULE1:

				if minormax is define.MAX:

					get_me_alive = board.calculate_alive(whoami)
					enemy_alive = board.calculate_alive(3-whoami)
					mydist = board.mydist(whoami, 1.1)
					enemydist = board.mydist(whoami, 1.3)
					myhomestate = board.homestate(whoami)

					return 18 * (get_me_alive-enemy_alive) + 3 * ( mydist-enemydist) + 1.2*myhomestate + random.random()


					
				else:
					get_me_alive = board.calculate_alive(3-whoami)
					enemy_alive = board.calculate_alive(whoami)
					mydist = board.mydist(3-whoami, 1.1)
					enemydist = board.mydist(3-whoami, 1.3)
					myhomestate = board.homestate(3-whoami)

					return 18 * (get_me_alive-enemy_alive) + 3 * ( mydist-enemydist) +1.2*myhomestate+ random.random()
			else:
				if minormax == define.MIN:
					whoami = 3-whoami

				get_me_alive = board.calculate_alive(whoami)
				enemy_alive = board.calculate_alive(3-whoami)
				if get_me_alive < 3:
					# loseeeeeeee, can not choose this
					return 0 + random.random()/5
				if enemy_alive < 3:
					# win!
					return 3000 + random.random()/5
				mydist = board.mydist(3-whoami, 1.1)
				enemydist = board.mydist(3-whoami, 1.2)
				myhomestate = board.homestate(3-whoami)
				return 5*(get_me_alive-enemy_alive) + mydist - enemydist + 0.5*myhomestate + random.random()/5

				

	def heursic_offensive(self, board, minormax, whoami, type):
		# self.node+=1
		if type == 1:
			if minormax == define.MAX:
				get_alive = board.calculate_alive(3-whoami)
				#print (get_alive)
				return 2*(30-get_alive) + random.random()
				#return board.calculate_naive(3-self.whoami)
			else:
				get_alive = board.calculate_alive(whoami)
				#print (get_alive)
				return 2*(30-get_alive) + random.random()
				#return board.calculate_naive(self.whoami)
		elif type == 2:
			if self.rule == define.RULE2:
				# minimize my opponent's pieces
				if minormax == define.MAX:
					

					get_enemy_alive = board.calculate_alive(3-whoami)
					get_me_alive = board.calculate_alive(whoami)

					mydist = board.mydist(whoami,1.3)
					enemydist = board.mydist(3-whoami, 1.3)

					return 10*(-get_enemy_alive + get_me_alive) + 2*(mydist-enemydist) + random.random()

				else:
					
					get_enemy_alive = board.calculate_alive(whoami)
					get_me_alive = board.calculate_alive(3-whoami)

					mydist = board.mydist(3-whoami,1.3)
					enemydist = board.mydist(whoami,1.3)

					return 10*(-get_enemy_alive + get_me_alive) + 2*(mydist-enemydist) + random.random()
			else:
				if minormax == define.MIN:
					whoami = 3-whoami
				get_me_alive = board.calculate_alive(whoami)
				enemy_alive = board.calculate_alive(3-whoami)
				if get_me_alive < 3:
					# loseeeeeeee, can not choose this
					return 0 + random.random()/5
				if enemy_alive < 3:
					# win!
					return 3000 + random.random()/5
				mydist = board.mydist(whoami, 1.3)
				enemydist = board.mydist(3-whoami, 1.1)
				return 5*(get_me_alive-enemy_alive) + (mydist - enemydist) + random.random()/5

			

	def ab_max(self, board, depth, minormax, minv, maxv, whoami):
		# self.node += 1
		if depth == self.depth:
			# for leaf node, just calculate the minmax value
			#print ("ab_max")
			if self.attack == define.DEFENSIVE:
				h = self.heursic_defensive(board, minormax, whoami, self.type)
			else:
				h = self.heursic_offensive(board, minormax, whoami, self.type)
			#print ("ab_max:",board.changestep)
			return (h, board)

		boards = board.next(whoami)
		ret_board = None
		temp_max = -np.inf
		self.node += 1
		'''
		for b in boards:
			print (b.state)
			print (b.changestep)
		'''
		if len(boards) == 0:
			if self.attack == define.DEFENSIVE:
				h = self.heursic_defensive(board, minormax, whoami, self.type)
			else:
				h = self.heursic_offensive(board, minormax, whoami, self.type)
			#print ("ab_max:",board.changestep)
			return (h, board)




		for b in boards:
			# cal min value via enemy
			#print ("call min")
			min_v = self.ab_min(b, depth+1, 1-minormax, minv, maxv, 3-whoami)
			if min_v is not None and min_v[0] > temp_max:
				temp_max = min_v[0]
				ret_board = min_v
			if temp_max >= maxv:
				return ret_board
			minv = max(minv, temp_max)
		#if depth < 2:
			#print ("ab_max_ret:",ret_board[1].changestep)
		if ret_board == None:
			print ("Panic, ab_max is returning None", depth,len(boards))
			print (board.state)
		return ret_board

	def ab_min(self, board, depth, minormax, minv, maxv, whoami):
		
		if depth == self.depth:
			# print ("ab_min")
			# print (self.whoami, self.attack,self.type)

			if self.attack == define.DEFENSIVE:
				h = self.heursic_defensive(board, minormax, whoami, self.type)
			else:
				#print ("!!!!")
				h = self.heursic_offensive(board, minormax, whoami, self.type)
			#print ("ab_min:",board.changestep)
			return (h, board)
		self.node += 1
		boards = board.next(whoami)

		if len(boards) == 0:
			if self.attack == define.DEFENSIVE:
				h = self.heursic_defensive(board, minormax, whoami, self.type)
			else:
				h = self.heursic_offensive(board, minormax, whoami, self.type)
			#print ("ab_max:",board.changestep)
			return (h, board)

		ret_board = None
		temp_min = np.inf
		for b in boards:
			#print ("call max")
			max_v = self.ab_max(b, depth+1, 1-minormax, minv, maxv, 3-whoami)

			#print (max_v)
			if max_v is not None and max_v[0] < temp_min:
				temp_min = max_v[0]
				ret_board = max_v
			if temp_min <= minv:
				return ret_board
			maxv = min(maxv, temp_min)
		#if depth < 2:
			#print ("ab_min_ret:",ret_board[1].changestep)
		if ret_board == None:
			print ("Panic, ab_min is returning None", depth, len(boards))
			print (board.state)
		return ret_board




