from board import board
from player import player
from time import time
import define


class breakthrough:
	# tie = head/tail
	def __init__(self, player1, player2, tie, boardtype):
		self.board = board(boardtype)
		self.player1 = player1
		self.player2 = player2
		self.turn = tie
		self.end = False
		self.winner = ''

	def check_end(self):
		if 1 in self.board.state[self.board.length-1]:
			self.end = True
			self.winner = 'player1'
		elif 2 in self.board.state[0]:
			self.end = True
			self.winner = 'player2'
		elif 1 not in self.board.state:
			self.end = True
			self.winner = 'player2'
		elif 2 not in self.board.state:
			self.end = True
			self.winner = 'player1'
		else:
			self.end = False

	def check_end_3(self):
		count_player1 = 0
		count_player2 = 0
		if self.board.capture1 == self.board.bothchess-2:
			self.end = True
			self.winner = 'player2'
			return
		if self.board.capture2 == self.board.bothchess-2:
			self.end = True
			self.winner = 'player1'
			return

		for x in range(self.board.width):
			if self.board.state[self.board.length-1][x] == define.PLAYER_1:
				count_player1 += 1
				if count_player1>=3:
					self.end = True
					self.winner = 'player1'
			elif self.board.state[0][x] == define.PLAYER_2:
				count_player2+=1
				if count_player2>=3:
					self.end = True
					self.winner = 'player2'

	'''
	def begin_pseudo(self):
		while self.end is False:
			if self.turn == define.PLAYER_TURN_1:
				# player 1's turn to play
				starttime = time()
				nextmove = self.player1.move(self.board)
				endtime = time()
				self.player1.time += endtime - starttime
				self.player1.step += 1
				self.check_end()
				self.turn = define.PLAYER_TURN_2
			else:
				# the same for player2
			self.board.move(nextmove)
			print (nextmove)
			print (self.board.state)
		# report the result
		print ("The winner is: {}".format(self.winner))

	'''


	def begin(self):
		while self.end is False:
			# player 1's turn
			if self.turn == define.PLAYER_TURN_1:
				print ("Player_1's turn")
				starttime = time()
				# get the next board
				nextmove = self.player1.move(self.board)
				print (nextmove)
				if nextmove is None:
					self.end = True
					self.winner = 'player2'
					continue
				endtime = time()
				self.player1.time += endtime - starttime
				self.board.move(nextmove[0],nextmove[1])
				self.player1.step+=1
				self.turn = define.PLAYER_TURN_2
				self.check_end()
			else:
				print ("Player_2's turn")
				starttime = time()
				# get the next board
				nextmove = self.player2.move(self.board)
				endtime = time()
				self.player2.time += endtime - starttime
				print (nextmove)
				if nextmove is None:
					self.end = True
					self.winner = 'player1'
					continue
				self.board.move(nextmove[0],nextmove[1])
				self.player2.step+=1
				self.turn = define.PLAYER_TURN_1
				self.check_end()
			print (self.board.state)
		print (self.board.state)
		print ("Game Over! The winner is:")
		print (self.winner)
		print ("==========================================")
		strategy = get_strategy(self.player1.strategy)
		attack = get_attack(self.player1.attack)
		print ("Player_1's strategy is {}, using {} {}".format(strategy, attack, self.player1.type))
		print ("Player_1 expanded {} nodes".format(self.player1.node))
		print ("Player_1 nodeExpand/move is {}".format(1.0*self.player1.node/self.player1.step))
		print ("Player_1 average move time is {}".format(1.0*self.player1.time/self.player1.step))
		print ("Player_1 has caputred {} opponents, moves in all is {}".format(self.board.capture2, self.player1.step))
		strategy = get_strategy(self.player2.strategy)
		attack = get_attack(self.player2.attack)
		print ("Player_2's strategy is {}, using {} {}".format(strategy, attack, self.player2.type))
		print ("Player_2 expanded {} nodes".format(self.player2.node))
		print ("Player_2 nodeExpand/move is {}".format(1.0*self.player2.node/self.player2.step))
		print ("Player_2 average move time is {}".format(1.0*self.player2.time/self.player2.step))
		print ("Player_2 has caputred {} opponents, moves in all is {}".format(self.board.capture1, self.player2.step))
		return self.winner


def get_strategy(input):
	if input == define.MINMAX:
		return "MINMAX"
	else:
		return "ALPHABETA"

def get_attack(input):
	if input == define.DEFENSIVE:
		return "DEFENSIVE"
	else:
		return "OFFENSIVE"

if __name__ == '__main__':
	p1 = 0
	p2 = 0
	total = 0
	while (True):
		player1 = player(define.RULE1, define.MINMAX, define.OFFENSIVE, 3, define.PLAYER_1, 1)
		player2 = player(define.RULE1, define.ALPHABETA, define.OFFENSIVE, 4, define.PLAYER_2, 1)
		game = breakthrough(player1, player2, define.PLAYER_TURN_1, define.SQUARE)
		winner = game.begin()
		if winner == 'player1':
			p1 += 1
		else:
			p2 += 1
		total+=1
		print ("rate:", p1*1.0/total,"total:",total)
		if total == 100:
			break
		#	print ("p1",p1,"\np2",p2)


